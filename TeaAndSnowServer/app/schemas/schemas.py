from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


# ==================== 通用响应 ====================

class ResponseModel(BaseModel):
    """通用响应包装"""
    code: int = 0
    message: str = "success"
    data: Optional[object] = None


# ==================== 用户 ====================

class UserNameUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=2, max_length=50)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: Optional[str] = None
    avatar_url: Optional[str] = None
    member_level: int = 0
    created_at: datetime


class WechatLoginIn(BaseModel):
    code: str = Field(..., min_length=1, description="wx.login 获取的临时 code")


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


# ==================== Banner ====================

class BannerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    image_url: str
    link_url: Optional[str] = None
    sort_order: int = 0


# ==================== 茶点分类 ====================

class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    sort_order: int = 0


# ==================== 茶点 ====================

class TeaItemBase(BaseModel):
    name: str
    short_desc: Optional[str] = None
    full_desc: Optional[str] = None
    small_image_url: Optional[str] = None
    large_image_url: Optional[str] = None
    base_price: Decimal


class TeaItemListOut(BaseModel):
    """茶点列表项（简洁）"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    name: str
    short_desc: Optional[str] = None
    small_image_url: Optional[str] = None
    base_price: Decimal


class TeaItemDetailOut(BaseModel):
    """茶点详情"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    category_id: int
    name: str
    short_desc: Optional[str] = None
    full_desc: Optional[str] = None
    small_image_url: Optional[str] = None
    large_image_url: Optional[str] = None
    base_price: Decimal


# ==================== 菜单 ====================

class MenuCategoryOut(BaseModel):
    """菜单分组（含茶点列表）"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    sort_order: int = 0
    tea_items: List[TeaItemListOut] = []


# ==================== 购物车 ====================

class CartItemCreate(BaseModel):
    tea_item_id: int
    quantity: int = Field(..., ge=1)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., ge=1)


class CartItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    tea_item_id: int
    quantity: int
    tea_item: Optional[TeaItemListOut] = None
    unit_price: Decimal = Decimal("0.00")
    subtotal: Decimal = Decimal("0.00")


class CartSummaryOut(BaseModel):
    items: List[CartItemOut] = []
    total_quantity: int = 0
    total_price: Decimal = Decimal("0.00")


class CartCheckoutOut(BaseModel):
    order_no: str
    total_amount: Decimal
    status: str


# ==================== 订单 ====================

class OrderItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tea_item_id: int
    tea_name: str
    small_image_url: Optional[str] = None
    quantity: int
    unit_price: Decimal


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_no: str
    total_amount: Decimal
    status: str
    created_at: datetime
    updated_at: datetime
    order_items: List[OrderItemOut] = []


class OrderPayOut(BaseModel):
    order_no: str
    status: str
    paid_at: datetime
