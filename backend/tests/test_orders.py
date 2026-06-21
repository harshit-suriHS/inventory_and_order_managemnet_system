from fastapi.testclient import TestClient


def _make_customer(client: TestClient) -> int:
    payload = {"full_name": "Ada", "email": "ada@example.com", "phone": "555"}
    return int(client.post("/customers", json=payload).json()["id"])


def _make_product(client: TestClient, sku: str, price: str, qty: int) -> int:
    payload = {"name": sku, "sku": sku, "price": price, "quantity": qty}
    return int(client.post("/products", json=payload).json()["id"])


def test_create_order_decrements_stock_and_computes_total(client: TestClient) -> None:
    customer = _make_customer(client)
    p1 = _make_product(client, "A", "10.00", 5)
    p2 = _make_product(client, "B", "2.50", 10)

    response = client.post(
        "/orders",
        json={
            "customer_id": customer,
            "items": [
                {"product_id": p1, "quantity": 2},
                {"product_id": p2, "quantity": 4},
            ],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["total_amount"] == "30.00"  # 2*10.00 + 4*2.50
    assert client.get(f"/products/{p1}").json()["quantity"] == 3
    assert client.get(f"/products/{p2}").json()["quantity"] == 6


def test_client_supplied_total_is_ignored(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "A", "10.00", 5)
    response = client.post(
        "/orders",
        json={
            "customer_id": customer,
            "total_amount": "0.01",
            "items": [{"product_id": product, "quantity": 1}],
        },
    )
    assert response.json()["total_amount"] == "10.00"


def test_insufficient_stock_rejected_without_side_effects(client: TestClient) -> None:
    customer = _make_customer(client)
    p1 = _make_product(client, "A", "10.00", 5)
    p2 = _make_product(client, "B", "2.50", 1)
    response = client.post(
        "/orders",
        json={
            "customer_id": customer,
            "items": [
                {"product_id": p1, "quantity": 2},
                {"product_id": p2, "quantity": 5},
            ],
        },
    )
    assert response.status_code == 409
    assert client.get(f"/products/{p1}").json()["quantity"] == 5  # unchanged
    assert client.get("/orders").json()["items"] == []


def test_order_for_missing_customer(client: TestClient) -> None:
    product = _make_product(client, "A", "10.00", 5)
    response = client.post(
        "/orders",
        json={"customer_id": 999, "items": [{"product_id": product, "quantity": 1}]},
    )
    assert response.status_code == 404


def test_order_for_missing_product(client: TestClient) -> None:
    customer = _make_customer(client)
    response = client.post(
        "/orders",
        json={"customer_id": customer, "items": [{"product_id": 999, "quantity": 1}]},
    )
    assert response.status_code == 404


def test_empty_items_rejected(client: TestClient) -> None:
    customer = _make_customer(client)
    response = client.post("/orders", json={"customer_id": customer, "items": []})
    assert response.status_code == 422


def test_duplicate_product_lines_exceeding_stock_rejected(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "A", "5.00", 4)
    response = client.post(
        "/orders",
        json={
            "customer_id": customer,
            "items": [
                {"product_id": product, "quantity": 3},
                {"product_id": product, "quantity": 3},
            ],
        },
    )
    assert response.status_code == 409
    assert client.get(f"/products/{product}").json()["quantity"] == 4  # unchanged
    assert client.get("/orders").json()["items"] == []


def test_duplicate_product_lines_within_stock_succeed(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "B", "3.00", 10)
    response = client.post(
        "/orders",
        json={
            "customer_id": customer,
            "items": [
                {"product_id": product, "quantity": 2},
                {"product_id": product, "quantity": 3},
            ],
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["total_amount"] == "15.00"  # (2+3) * 3.00
    assert len(body["items"]) == 2
    assert client.get(f"/products/{product}").json()["quantity"] == 5  # 10 - 5


def test_order_includes_nested_product_and_customer(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "A", "10.00", 5)
    created = client.post(
        "/orders",
        json={"customer_id": customer, "items": [{"product_id": product, "quantity": 2}]},
    ).json()

    detail = client.get(f"/orders/{created['id']}").json()
    assert detail["customer"] == {"id": customer, "full_name": "Ada"}
    item = detail["items"][0]
    assert item["product"] == {"id": product, "name": "A", "sku": "A"}
    assert item["quantity"] == 2
    assert item["unit_price"] == "10.00"


def test_get_and_delete_order(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "A", "10.00", 5)
    created = client.post(
        "/orders",
        json={"customer_id": customer, "items": [{"product_id": product, "quantity": 1}]},
    ).json()
    assert client.get(f"/orders/{created['id']}").status_code == 200
    assert client.delete(f"/orders/{created['id']}").status_code == 204
    assert client.get(f"/orders/{created['id']}").status_code == 404
