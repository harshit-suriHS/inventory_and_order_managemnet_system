from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Product]:
        return list(self.db.scalars(select(Product).order_by(Product.id)))

    def get(self, product_id: int) -> Product | None:
        return self.db.get(Product, product_id)

    def get_by_sku(self, sku: str) -> Product | None:
        return self.db.scalar(select(Product).where(Product.sku == sku))

    def add(self, product: Product) -> Product:
        self.db.add(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
