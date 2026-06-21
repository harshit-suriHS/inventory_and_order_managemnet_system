from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import Pagination, pagination_params
from app.schemas.order import OrderCreate, OrderRead, OrderSummaryRead
from app.schemas.pagination import Page
from app.services.order_service import OrderService

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("", response_model=Page[OrderSummaryRead])
def list_orders(
    pagination: Pagination = Depends(pagination_params), db: Session = Depends(get_db)
) -> object:
    service = OrderService(db)
    return Page(
        items=service.list(pagination.limit, pagination.offset),
        total=service.count(),
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/{order_id}", response_model=OrderRead)
def get_order(order_id: int, db: Session = Depends(get_db)) -> object:
    return OrderService(db).get(order_id)


@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(data: OrderCreate, db: Session = Depends(get_db)) -> object:
    return OrderService(db).create(data)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(order_id: int, db: Session = Depends(get_db)) -> None:
    OrderService(db).cancel(order_id)
