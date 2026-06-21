from decimal import Decimal

from sqlalchemy.orm import Session

from app.exceptions import InsufficientStockError, NotFoundError
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.repositories.customer_repository import CustomerRepository
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.schemas.order import OrderCreate


class OrderService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.orders = OrderRepository(db)
        self.products = ProductRepository(db)
        self.customers = CustomerRepository(db)

    def list(self, limit: int, offset: int) -> list[Order]:
        return self.orders.list(limit, offset)

    def count(self) -> int:
        return self.orders.count()

    def get(self, order_id: int) -> Order:
        order = self.orders.get(order_id)
        if order is None:
            raise NotFoundError(f"Order {order_id} not found")
        return order

    def create(self, data: OrderCreate) -> Order:
        customer = self.customers.get(data.customer_id)
        if customer is None:
            raise NotFoundError(f"Customer {data.customer_id} not found")

        # Resolve products and accumulate cumulative demand per product_id so
        # that duplicate lines are validated against their combined quantity.
        products: dict[int, Product] = {}
        cumulative_demand: dict[int, int] = {}
        for line in data.items:
            if line.product_id not in products:
                product = self.products.get(line.product_id)
                if product is None:
                    raise NotFoundError(f"Product {line.product_id} not found")
                products[line.product_id] = product
                cumulative_demand[line.product_id] = 0
            cumulative_demand[line.product_id] += line.quantity

        # Validate all products before mutating anything.
        for product_id, total_qty in cumulative_demand.items():
            product = products[product_id]
            if product.quantity < total_qty:
                raise InsufficientStockError(
                    f"Insufficient stock for product {product_id} "
                    f"(have {product.quantity}, need {total_qty})"
                )

        # Decrement stock once per product by its cumulative demand.
        for product_id, total_qty in cumulative_demand.items():
            products[product_id].quantity -= total_qty

        # Build one OrderItem per input line; total is sum over all lines.
        order = Order(customer=customer)
        total = Decimal("0")
        for line in data.items:
            product = products[line.product_id]
            order.items.append(
                OrderItem(
                    product=product,
                    quantity=line.quantity,
                    unit_price=product.price,
                )
            )
            total += product.price * line.quantity

        order.total_amount = total
        self.orders.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def delete(self, order_id: int) -> None:
        order = self.get(order_id)
        self.orders.delete(order)
        self.db.commit()
