from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_users():
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user():
    user = {
        "id": 1,
        "name": "Ana",
        "email": "ana@email.com"
    }

    response = client.post("/users", json=user)

    assert response.status_code == 200
    assert response.json()["name"] == "Ana"
    assert response.json()["email"] == "ana@email.com"


def test_get_user():
    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_delete_user():
    response = client.delete("/users/1")

    assert response.status_code == 200