from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Order, OrderItem
from app.models.models import User
from app.schemas.schemas import OrderOut, OrderItemOut, ResponseModel
from app.utils.auth import require_user

router = APIRouter(prefix="/api/orders", tags=["订单"])


@router.get("", response_model=ResponseModel)
def list_orders(
    status: str | None = None,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """查询用户订单列表"""
    query = db.query(Order).filter(Order.user_id == current_user.id)
    if status:
        query = query.filter(Order.status == status)

    orders = query.order_by(Order.created_at.desc()).all()

    result: List[OrderOut] = []
    for order in orders:
        items = _build_order_items(db, order)
        result.append(
            OrderOut(
                id=order.id,
                order_no=order.order_no,
                total_amount=order.total_amount,
                status=order.status,
                created_at=order.created_at,
                updated_at=order.updated_at,
                order_items=items,
            )
        )

    return ResponseModel(data=result)


@router.get("/{order_no}", response_model=ResponseModel)
def get_order_detail(
    order_no: str,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """查询订单详情"""
    order = (
        db.query(Order)
        .filter(Order.order_no == order_no, Order.user_id == current_user.id)
        .first()
    )
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在",
        )

    items = _build_order_items(db, order)
    return ResponseModel(
        data=OrderOut(
            id=order.id,
            order_no=order.order_no,
            total_amount=order.total_amount,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            order_items=items,
        )
    )


@router.post("/{order_no}/pay", response_model=ResponseModel)
def pay_order(
    order_no: str,
    current_user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    """支付订单（模拟支付，小程序调用后订单转入已制作状态）"""
    order = (
        db.query(Order)
        .filter(Order.order_no == order_no, Order.user_id == current_user.id)
        .first()
    )
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="订单不存在",
        )

    if order.status != "pending":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"订单状态为 {order.status}，无法支付",
        )

    order.status = "paid"
    db.commit()
    db.refresh(order)

    from app.schemas.schemas import OrderPayOut
    return ResponseModel(
        data=OrderPayOut(
            order_no=order.order_no,
            status=order.status,
            paid_at=order.updated_at,
        )
    )


def _build_order_items(db: Session, order: Order) -> List[OrderItemOut]:
    """构建订单项输出"""
    items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()
    result: List[OrderItemOut] = []
    for item in items:
        result.append(
            OrderItemOut(
                id=item.id,
                tea_item_id=item.tea_item_id,
                tea_name=item.tea_name,
                small_image_url=item.small_image_url,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
        )
    return result
