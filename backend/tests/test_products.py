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
    assert len(response.json()) == 2


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


def test_delete_product(client: TestClient) -> None:
    created = client.post("/products", json=_payload()).json()
    assert client.delete(f"/products/{created['id']}").status_code == 204
    assert client.get(f"/products/{created['id']}").status_code == 404
