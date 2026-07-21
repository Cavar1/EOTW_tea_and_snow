import httpx
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import (
    ResponseModel,
    TokenOut,
    UserOut,
    UserNameUpdate,
    WechatLoginIn,
)
from app.utils.auth import create_access_token, require_user
from app.utils.upload import save_upload_file

router = APIRouter(prefix="/api/users", tags=["用户"])

WECHAT_JSCODE2SESSION_URL = "https://api.weixin.qq.com/sns/jscode2session"


@router.post("/login", response_model=ResponseModel)
async def wechat_login(login_in: WechatLoginIn, db: Session = Depends(get_db)):
    """微信小程序静默登录：用 code 换取 openid，自动注册或更新用户并下发令牌"""
    settings = get_settings()

    if not settings.wechat_appid or not settings.wechat_appsecret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务端未配置微信小程序凭据",
        )

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            WECHAT_JSCODE2SESSION_URL,
            params={
                "appid": settings.wechat_appid,
                "secret": settings.wechat_appsecret,
                "js_code": login_in.code,
                "grant_type": "authorization_code",
            },
            timeout=10.0,
        )
        data = resp.json()

    if data.get("errcode"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"微信接口错误: {data.get('errmsg', data)}",
        )

    openid = data.get("openid")
    session_key = data.get("session_key")
    if not openid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法获取用户 openid",
        )

    user = db.query(User).filter(User.openid == openid).first()
    if not user:
        user = User(
            openid=openid,
            session_key=session_key,
            member_level=0,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.session_key = session_key
        db.commit()
        db.refresh(user)

    token = create_access_token({"sub": str(user.id)})
    return ResponseModel(
        data=TokenOut(
            access_token=token,
            user=UserOut.model_validate(user),
        )
    )


@router.get("/me", response_model=ResponseModel)
def get_me(current_user: User = Depends(require_user)):
    """查询当前登录用户（用户名、头像、会员等级）"""
    return ResponseModel(data=UserOut.model_validate(current_user))


@router.put("/me", response_model=ResponseModel)
def update_me(
    user_in: UserNameUpdate,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """修改当前用户名字"""
    if user_in.username is not None and user_in.username != current_user.username:
        current_user.username = user_in.username

    db.commit()
    db.refresh(current_user)
    return ResponseModel(data=UserOut.model_validate(current_user))


@router.post("/me/avatar", response_model=ResponseModel)
def upload_avatar(
    file: UploadFile = File(...),
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """上传用户头像并自动更新头像链接"""
    try:
        avatar_url = save_upload_file(file, subfolder="users/avatar")
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    current_user.avatar_url = avatar_url
    db.commit()
    db.refresh(current_user)
    return ResponseModel(data=UserOut.model_validate(current_user))
