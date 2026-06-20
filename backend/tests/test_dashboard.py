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
