from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, limit: int, offset: int) -> list[Product]:
        stmt = select(Product).order_by(Product.id).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    def count(self) -> int:
        return int(self.db.scalar(select(func.count()).select_from(Product)) or 0)

    def count_active(self) -> int:
        stmt = select(func.count()).select_from(Product).where(Product.status == "active")
        return int(self.db.scalar(stmt) or 0)

    def list_low_stock(self, threshold: int) -> Sequence[Product]:
        stmt = (
            select(Product)
            .where(Product.status == "active", Product.quantity < threshold)
            .order_by(Product.quantity)
        )
        return list(self.db.scalars(stmt))

    def get(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_by_sku(self, sku: str) -> Product | None:
        return self.db.scalar(select(Product).where(Product.sku == sku))

    def add(self, product: Product) -> Product:
        self.db.add(product)
        return product
