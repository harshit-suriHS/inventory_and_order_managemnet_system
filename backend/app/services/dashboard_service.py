from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.db = db

    def _count(self, model: type) -> int:
        return int(self.db.scalar(select(func.count()).select_from(model)) or 0)

    def summary(self) -> dict[str, object]:
        low_stock = list(
            self.db.scalars(
                select(Product)
                .where(Product.quantity < get_settings().low_stock_threshold)
                .order_by(Product.quantity)
            )
        )
        return {
            "total_products": self._count(Product),
            "total_customers": self._count(Customer),
            "total_orders": self._count(Order),
            "low_stock_products": low_stock,
        }
