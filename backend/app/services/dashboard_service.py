from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.repositories.customer_repository import CustomerRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.products = ProductRepository(db)
        self.customers = CustomerRepository(db)
        self.orders = OrderRepository(db)

    def summary(self) -> dict[str, object]:
        return {
            "total_products": self.products.count_active(),
            "total_customers": self.customers.count_active(),
            "total_orders": self.orders.count_active(),
            "low_stock_products": self.products.list_low_stock(
                get_settings().low_stock_threshold
            ),
        }
