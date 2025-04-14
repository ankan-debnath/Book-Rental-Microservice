from fastapi.testclient import TestClient

from app.api.main import app
from app.api.main import PORT

client = TestClient(app)


def test_user__root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == f"Server is running at port {PORT}"

def test_user_register():
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

def test_user_duplicate_register():
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

def test_user_get():
    token_response = client.post(
        url="/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username" : "demo@example.com",
            "password": "demo_password"
        }
    )
    assert token_response.status_code == 200
    access_token = token_response.json()["access_token"]

    user_response = client.get(
        "/v1/user/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    assert user_response.status_code == 200
    content = user_response.json()
    data = content.get("data", None)

    assert content.get("success", False)
    assert content.get("message", None) == "User fetched successfully."
    assert len(data.get("user_id", "")) == 36
    assert data.get("name", None) == "demo_user"
    assert data.get("email", None) == "demo@example.com"

def test_user_put():
    token_response = client.post(
        url="/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "demo@example.com",
            "password": "demo_password"
        }
    )
    assert token_response.status_code == 200
    access_token = token_response.json()["access_token"]

    user_response = client.put(
        "/v1/user/me",
        headers={ "Authorization": f"Bearer {access_token}" },
        json = {
            "name": "new_demo",
            "email": "new_demo@example.com",
            "password": "new_demo_password"
        }
    )

    content = user_response.json()
    data = content.get("data", None)

    assert user_response.status_code == 200
    content = user_response.json()
    data = content.get("data", None)

    assert content.get("success", False)
    assert content.get("message", None) == 'User updated successfully'
    assert len(data.get("user_id", "")) == 36
    assert data.get("name", None) == 'new_demo'
    assert data.get("email", None) == 'new_demo@example.com'
