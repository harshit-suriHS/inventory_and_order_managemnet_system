from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import Pagination, pagination_params
from app.schemas.pagination import Page
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services.product_service import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=Page[ProductRead])
def list_products(
    pagination: Pagination = Depends(pagination_params), db: Session = Depends(get_db)
) -> object:
    service = ProductService(db)
    return Page(
        items=service.list(pagination.limit, pagination.offset),
        total=service.count(),
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)) -> object:
    return ProductService(db).get(product_id)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db)) -> object:
    return ProductService(db).create(data)


@router.put("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int, data: ProductUpdate, db: Session = Depends(get_db)
) -> object:
    return ProductService(db).update(product_id, data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    ProductService(db).delete(product_id)
