from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.order import Order


class OrderRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Order]:
        return list(self.db.scalars(select(Order).order_by(Order.id)))

    def get(self, order_id: int) -> Order | None:
        return self.db.get(Order, order_id)

    def add(self, order: Order) -> Order:
        self.db.add(order)
        return order

    def delete(self, order: Order) -> None:
        self.db.delete(order)
