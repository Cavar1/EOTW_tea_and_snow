from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.database import Base, engine
from app.routers import cart, menu, order, user

# 尝试创建数据库表（如果不存在）
# try:
#     Base.metadata.create_all(bind=engine)
# except Exception as e:
#     import logging
#     logging.warning(f"数据库自动建表失败（可能是数据库未启动或连接配置错误）: {e}")

app = FastAPI(
    title="TeaAndSnow API",
    description="奈茶的雪点单小程序后端",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 路由注册
app.include_router(menu.router)
app.include_router(user.router)
app.include_router(cart.router)
app.include_router(order.router)


@app.get("/")
async def root():
    return {"message": "某个人进奈茶的雪店看了一眼然后转身就走..."}
