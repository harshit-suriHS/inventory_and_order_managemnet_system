from fastapi.testclient import TestClient


def _payload(**overrides: object) -> dict[str, object]:
    base = {"name": "Widget", "sku": "WID-1", "price": "9.99", "quantity": 5}
    base.update(overrides)
    return base


def test_create_product(client: TestClient) -> None:
    response = client.post("/products", json=_payload())
    assert response.status_code == 201
    body = response.json()
    assert body["sku"] == "WID-1"
    assert body["id"] > 0


def test_duplicate_sku_conflicts(client: TestClient) -> None:
    client.post("/products", json=_payload())
    response = client.post("/products", json=_payload(name="Other"))
    assert response.status_code == 409


def test_negative_quantity_rejected(client: TestClient) -> None:
    response = client.post("/products", json=_payload(quantity=-1))
    assert response.status_code == 422


def test_negative_price_rejected(client: TestClient) -> None:
    response = client.post("/products", json=_payload(price="-1.00"))
    assert response.status_code == 422


def test_list_products(client: TestClient) -> None:
    client.post("/products", json=_payload())
    client.post("/products", json=_payload(sku="WID-2"))
    response = client.get("/products")
    assert response.status_code == 200
    body = response.json()
    assert body["total"] == 2
    assert len(body["items"]) == 2


def test_list_products_pagination(client: TestClient) -> None:
    client.post("/products", json=_payload(sku="WID-1"))
    client.post("/products", json=_payload(sku="WID-2"))
    client.post("/products", json=_payload(sku="WID-3"))

    response = client.get("/products?limit=2&offset=0")
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 2
    assert body["total"] == 3
    assert body["limit"] == 2
    assert body["offset"] == 0

    response = client.get("/products?limit=2&offset=2")
    assert response.status_code == 200
    body = response.json()
    assert len(body["items"]) == 1
    assert body["total"] == 3
    assert body["offset"] == 2


def test_list_limit_validation(client: TestClient) -> None:
    assert client.get("/products?limit=0").status_code == 422
    assert client.get("/products?limit=101").status_code == 422


def test_get_missing_product(client: TestClient) -> None:
    assert client.get("/products/999").status_code == 404


def test_update_product(client: TestClient) -> None:
    created = client.post("/products", json=_payload()).json()
    response = client.put(
        f"/products/{created['id']}", json=_payload(name="Renamed", price="12.50")
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Renamed"


def test_update_to_duplicate_sku_conflicts(client: TestClient) -> None:
    client.post("/products", json=_payload(sku="WID-1"))
    other = client.post("/products", json=_payload(sku="WID-2")).json()
    response = client.put(f"/products/{other['id']}", json=_payload(sku="WID-1"))
    assert response.status_code == 409


def test_delete_archives_product(client: TestClient) -> None:
    created = client.post("/products", json=_payload()).json()
    assert created["status"] == "active"
    assert client.delete(f"/products/{created['id']}").status_code == 204
    fetched = client.get(f"/products/{created['id']}")
    assert fetched.status_code == 200  # archived, not removed
    assert fetched.json()["status"] == "archived"


def test_restore_product_via_put(client: TestClient) -> None:
    created = client.post("/products", json=_payload()).json()
    client.delete(f"/products/{created['id']}")
    restored = client.put(f"/products/{created['id']}", json=_payload(status="active"))
    assert restored.status_code == 200
    assert restored.json()["status"] == "active"
