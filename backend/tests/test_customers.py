from fastapi.testclient import TestClient


def _payload(**overrides: object) -> dict[str, object]:
    base = {"full_name": "Ada Lovelace", "email": "ada@example.com", "phone": "555-0100"}
    base.update(overrides)
    return base


def test_create_customer(client: TestClient) -> None:
    response = client.post("/customers", json=_payload())
    assert response.status_code == 201
    assert response.json()["email"] == "ada@example.com"


def test_duplicate_email_conflicts(client: TestClient) -> None:
    client.post("/customers", json=_payload())
    response = client.post("/customers", json=_payload(full_name="Other"))
    assert response.status_code == 409


def test_invalid_email_rejected(client: TestClient) -> None:
    response = client.post("/customers", json=_payload(email="not-an-email"))
    assert response.status_code == 422


def test_list_and_get_customer(client: TestClient) -> None:
    created = client.post("/customers", json=_payload()).json()
    assert client.get("/customers").status_code == 200
    assert client.get(f"/customers/{created['id']}").json()["id"] == created["id"]


def test_get_missing_customer(client: TestClient) -> None:
    assert client.get("/customers/999").status_code == 404


def test_delete_customer(client: TestClient) -> None:
    created = client.post("/customers", json=_payload()).json()
    assert client.delete(f"/customers/{created['id']}").status_code == 204
    assert client.get(f"/customers/{created['id']}").status_code == 404
