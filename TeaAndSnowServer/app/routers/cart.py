from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Cart, TeaItem
from app.models.models import User
from app.schemas.schemas import CartCheckoutOut, CartItemCreate, CartItemOut, CartItemUpdate, CartSummaryOut, ResponseModel
from app.utils.auth import require_user

router = APIRouter(prefix="/api/cart", tags=["购物车"])


def schemas_tea_item_list(tea_item: TeaItem):
    from app.schemas.schemas import TeaItemListOut
    return TeaItemListOut.model_validate(tea_item)


def _build_cart_summary(db: Session, carts: List[Cart]) -> CartSummaryOut:
    """构建购物车摘要"""
    items_out: List[CartItemOut] = []
    total_price = Decimal("0.00")
    total_qty = 0

    for cart in carts:
        tea_item = cart.tea_item
        unit_price = tea_item.base_price if tea_item else Decimal("0.00")
        subtotal = unit_price * cart.quantity

        items_out.append(
            CartItemOut(
                id=cart.id,
                user_id=cart.user_id,
                tea_item_id=cart.tea_item_id,
                quantity=cart.quantity,
                tea_item=schemas_tea_item_list(tea_item) if tea_item else None,
                unit_price=unit_price,
                subtotal=subtotal,
            )
        )
        total_price += subtotal
        total_qty += cart.quantity

    return CartSummaryOut(items=items_out, total_quantity=total_qty, total_price=total_price)


@router.get("", response_model=ResponseModel)
def get_cart(
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """查询购物车内容"""
    carts = (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id)
        .order_by(Cart.created_at.desc())
        .all()
    )
    # 预加载茶点
    for c in carts:
        _ = c.tea_item

    summary = _build_cart_summary(db, carts)
    return ResponseModel(data=summary)


@router.post("", response_model=ResponseModel)
def add_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """添加茶点到购物车"""
    tea_item = db.query(TeaItem).filter(TeaItem.id == item.tea_item_id, TeaItem.is_active == True).first()
    if not tea_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="茶点不存在",
        )

    # 查找是否已有相同茶点的购物车记录，有则数量累加
    existing = (
        db.query(Cart)
        .filter(
            Cart.user_id == current_user.id,
            Cart.tea_item_id == item.tea_item_id,
        )
        .first()
    )

    if existing:
        existing.quantity += item.quantity
        db.commit()
        db.refresh(existing)
        return ResponseModel(data=_build_cart_summary(db, [existing]))

    # 新建购物车记录
    cart = Cart(
        user_id=current_user.id,
        tea_item_id=item.tea_item_id,
        quantity=item.quantity,
    )
    db.add(cart)
    db.commit()
    db.refresh(cart)

    return ResponseModel(data=_build_cart_summary(db, [cart]))


@router.put("/{cart_id}", response_model=ResponseModel)
def update_cart_item(
    cart_id: int,
    item: CartItemUpdate,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """修改已添加茶点的数量"""
    cart = (
        db.query(Cart)
        .filter(Cart.id == cart_id, Cart.user_id == current_user.id)
        .first()
    )
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="购物车项不存在",
        )

    cart.quantity = item.quantity
    db.commit()
    db.refresh(cart)

    return ResponseModel(data=_build_cart_summary(db, [cart]))


@router.delete("/{cart_id}", response_model=ResponseModel)
def delete_cart_item(
    cart_id: int,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """删除购物车中的茶点"""
    cart = (
        db.query(Cart)
        .filter(Cart.id == cart_id, Cart.user_id == current_user.id)
        .first()
    )
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="购物车项不存在",
        )

    db.delete(cart)
    db.commit()
    return ResponseModel(data=None)


@router.post("/checkout", response_model=ResponseModel)
def checkout_cart(
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """结算购物车：生成订单，清空购物车"""
    from app.models.models import Order, OrderItem
    import uuid
    from datetime import datetime

    carts = (
        db.query(Cart)
        .filter(Cart.user_id == current_user.id)
        .all()
    )
    if not carts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="购物车为空",
        )

    # 预加载茶点
    for c in carts:
        _ = c.tea_item

    summary = _build_cart_summary(db, carts)

    # 生成订单号
    order_no = f"TAS{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"

    order = Order(
        user_id=current_user.id,
        order_no=order_no,
        total_amount=summary.total_price,
        status="pending",
    )
    db.add(order)
    db.flush()  # 获取order.id

    for item in summary.items:
        tea_item = db.query(TeaItem).filter(TeaItem.id == item.tea_item_id).first()
        order_item = OrderItem(
            order_id=order.id,
            tea_item_id=item.tea_item_id,
            tea_name=tea_item.name if tea_item else "",
            small_image_url=tea_item.small_image_url if tea_item else None,
            quantity=item.quantity,
            unit_price=item.unit_price,
        )
        db.add(order_item)

    # 清空购物车
    for c in carts:
        db.delete(c)

    db.commit()
    db.refresh(order)

    return ResponseModel(
        data=CartCheckoutOut(
            order_no=order.order_no,
            total_amount=order.total_amount,
            status=order.status,
        )
    )
