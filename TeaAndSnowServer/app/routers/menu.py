from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Banner, Category, TeaItem
from app.schemas.schemas import (
    BannerOut,
    MenuCategoryOut,
    ResponseModel,
    TeaItemDetailOut,
    TeaItemListOut,
)

router = APIRouter(prefix="/api", tags=["菜单"])


@router.get("/banners", response_model=ResponseModel)
def get_banners(db: Session = Depends(get_db)):
    """获取首页横幅图列表"""
    banners = (
        db.query(Banner)
        .filter(Banner.is_active == True)
        .order_by(Banner.sort_order.asc())
        .all()
    )
    return ResponseModel(data=[BannerOut.model_validate(b) for b in banners])


@router.get("/menu", response_model=ResponseModel)
def get_menu(db: Session = Depends(get_db)):
    """获取菜单（分类 + 茶点列表）"""
    categories = (
        db.query(Category)
        .filter(Category.is_active == True)
        .order_by(Category.sort_order.asc())
        .all()
    )

    result: List[MenuCategoryOut] = []
    for cat in categories:
        tea_items = (
            db.query(TeaItem)
            .filter(TeaItem.category_id == cat.id, TeaItem.is_active == True)
            .order_by(TeaItem.created_at.asc())
            .all()
        )
        result.append(
            MenuCategoryOut(
                id=cat.id,
                name=cat.name,
                description=cat.description,
                sort_order=cat.sort_order,
                tea_items=[TeaItemListOut.model_validate(t) for t in tea_items],
            )
        )

    return ResponseModel(data=result)


@router.get("/tea-items/{tea_item_id}", response_model=ResponseModel)
def get_tea_item_detail(tea_item_id: int, db: Session = Depends(get_db)):
    """获取茶点详情"""
    tea_item = (
        db.query(TeaItem)
        .filter(TeaItem.id == tea_item_id, TeaItem.is_active == True)
        .first()
    )
    if not tea_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="茶点不存在",
        )

    return ResponseModel(data=TeaItemDetailOut.model_validate(tea_item))
