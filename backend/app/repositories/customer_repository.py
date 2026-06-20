from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Customer]:
        return list(self.db.scalars(select(Customer).order_by(Customer.id)))

    def get(self, customer_id: int) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def get_by_email(self, email: str) -> Customer | None:
        return self.db.scalar(select(Customer).where(Customer.email == email))

    def add(self, customer: Customer) -> Customer:
        self.db.add(customer)
        return customer

    def delete(self, customer: Customer) -> None:
        self.db.delete(customer)
