from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = ProductRepository(db)

    def list(self, limit: int, offset: int) -> list[Product]:
        return self.repo.list(limit, offset)

    def count(self) -> int:
        return self.repo.count()

    def get(self, product_id: int) -> Product:
        product = self.repo.get(product_id)
        if product is None:
            raise NotFoundError(f"Product {product_id} not found")
        return product

    def create(self, data: ProductCreate) -> Product:
        if self.repo.get_by_sku(data.sku) is not None:
            raise ConflictError(f"SKU '{data.sku}' already exists")
        product = self.repo.add(Product(**data.model_dump()))
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product_id: int, data: ProductUpdate) -> Product:
        product = self.get(product_id)
        existing = self.repo.get_by_sku(data.sku)
        if existing is not None and existing.id != product_id:
            raise ConflictError(f"SKU '{data.sku}' already exists")
        for field, value in data.model_dump().items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product_id: int) -> None:
        product = self.get(product_id)
        self.repo.delete(product)
        self.db.commit()
