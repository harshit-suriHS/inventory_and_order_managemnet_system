from sqlalchemy.orm import Session

from app.exceptions import ConflictError, NotFoundError
from app.models.customer import Customer
from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate


class CustomerService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = CustomerRepository(db)

    def list_all(self) -> list[Customer]:
        return self.repo.list()

    def get(self, customer_id: int) -> Customer:
        customer = self.repo.get(customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {customer_id} not found")
        return customer

    def create(self, data: CustomerCreate) -> Customer:
        if self.repo.get_by_email(data.email) is not None:
            raise ConflictError(f"Email '{data.email}' already exists")
        customer = self.repo.add(Customer(**data.model_dump()))
        self.db.commit()
        self.db.refresh(customer)
        return customer

    def delete(self, customer_id: int) -> None:
        customer = self.get(customer_id)
        self.repo.delete(customer)
        self.db.commit()
