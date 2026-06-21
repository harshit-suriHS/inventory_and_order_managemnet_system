from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.order import Order


class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, limit: int, offset: int) -> list[Order]:
        return list(self.db.scalars(select(Order).order_by(Order.id).limit(limit).offset(offset)))

    def count(self) -> int:
        return int(self.db.scalar(select(func.count()).select_from(Order)) or 0)

    def count_active(self) -> int:
        stmt = select(func.count()).select_from(Order).where(Order.status == "active")
        return int(self.db.scalar(stmt) or 0)

    def get(self, order_id: int) -> Order | None:
        return self.db.get(Order, order_id)

    def add(self, order: Order) -> Order:
        self.db.add(order)
        return order
