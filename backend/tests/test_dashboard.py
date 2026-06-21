from fastapi.testclient import TestClient


def test_dashboard_summary(client: TestClient) -> None:
    client.post("/customers", json={"full_name": "Ada", "email": "a@e.com", "phone": "1"})
    client.post("/products", json={"name": "Low", "sku": "LOW", "price": "1.00", "quantity": 2})
    client.post("/products", json={"name": "High", "sku": "HIGH", "price": "1.00", "quantity": 50})

    response = client.get("/dashboard")
    assert response.status_code == 200
    body = response.json()
    assert body["total_products"] == 2
    assert body["total_customers"] == 1
    assert body["total_orders"] == 0
    skus = {p["sku"] for p in body["low_stock_products"]}
    assert skus == {"LOW"}  # default threshold 10


def test_dashboard_excludes_archived_and_cancelled(client: TestClient) -> None:
    cust = client.post(
        "/customers", json={"full_name": "Ada", "email": "a@e.com", "phone": "1"}
    ).json()
    archived_cust = client.post(
        "/customers", json={"full_name": "Bob", "email": "b@e.com", "phone": "2"}
    ).json()
    client.delete(f"/customers/{archived_cust['id']}")

    active_prod = client.post(
        "/products", json={"name": "A", "sku": "A", "price": "1.00", "quantity": 50}
    ).json()
    archived_low = client.post(
        "/products", json={"name": "B", "sku": "B", "price": "1.00", "quantity": 2}
    ).json()
    client.delete(f"/products/{archived_low['id']}")  # archived AND low stock

    order = client.post(
        "/orders",
        json={
            "customer_id": cust["id"],
            "items": [{"product_id": active_prod["id"], "quantity": 1}],
        },
    ).json()
    client.delete(f"/orders/{order['id']}")  # cancel

    body = client.get("/dashboard").json()
    assert body["total_customers"] == 1  # archived excluded
    assert body["total_products"] == 1  # archived excluded
    assert body["total_orders"] == 0  # cancelled excluded
    assert body["low_stock_products"] == []  # archived low-stock excluded
