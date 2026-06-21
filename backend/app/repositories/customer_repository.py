from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self, limit: int, offset: int) -> list[Customer]:
        stmt = select(Customer).order_by(Customer.id).limit(limit).offset(offset)
        return list(self.db.scalars(stmt))

    def count(self) -> int:
        return int(self.db.scalar(select(func.count()).select_from(Customer)) or 0)

    def get(self, customer_id: int) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def get_by_email(self, email: str) -> Customer | None:
        return self.db.scalar(select(Customer).where(Customer.email == email))

    def add(self, customer: Customer) -> Customer:
        self.db.add(customer)
        return customer

    def delete(self, customer: Customer) -> None:
        self.db.delete(customer)
