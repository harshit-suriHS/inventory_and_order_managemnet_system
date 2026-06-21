from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies import Pagination, pagination_params
from app.schemas.customer import CustomerCreate, CustomerRead
from app.schemas.pagination import Page
from app.services.customer_service import CustomerService

router = APIRouter(prefix="/customers", tags=["customers"])


@router.get("", response_model=Page[CustomerRead])
def list_customers(
    pagination: Pagination = Depends(pagination_params), db: Session = Depends(get_db)
) -> object:
    service = CustomerService(db)
    return Page(
        items=service.list(pagination.limit, pagination.offset),
        total=service.count(),
        limit=pagination.limit,
        offset=pagination.offset,
    )


@router.get("/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)) -> object:
    return CustomerService(db).get(customer_id)


@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)) -> object:
    return CustomerService(db).create(data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
    CustomerService(db).delete(customer_id)
