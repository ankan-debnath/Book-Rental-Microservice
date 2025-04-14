from fastapi.testclient import TestClient

from app.api.main import app
from app.api.main import PORT

client = TestClient(app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == f"Server is running at port {PORT}"


def test_register_route():
    user = "demo_user"
    email = "demo@example.com"
    response = client.post(
        "/v1/user",
            json={
            "name" : user,
            "email" : email,
            "password" : "demo_password"
        }
    )
    data = response.json()

    assert response.status_code == 201

    assert data["success"]
    assert data["message"] == "User created successfully"
    assert len(data["data"]["user_id"]) == 36
    assert data["data"]["name"] == user
    assert data["data"]["email"] == email

# @pytest.mark.xfail
def test_duplicate_register_route():
    user = "demo_user"
    email = "demo@example.com"
    response = client.post(
        "/v1/user",
            json={
            "name" : user,
            "email" : email,
            "password" : "demo_password"
        }
    )

    assert response.status_code == 400
    data = response.json()

    assert not data["success"]
    assert data["message"] == f"A user with email '{email}' already exists."
    assert not data["data"]
    assert data["error_code"] == "USER_ALREADY_EXISTS"


