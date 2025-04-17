from .conftest import client
from .conftest import PORT


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
    assert response.status_code == 201

    content = response.json()
    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'User created successfully'
    assert len(data.get("user_id", "")) == 36
    assert data.get("name", "") == user
    assert data.get("email", "") == email

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
    content = response.json()

    assert not content.get("success", True)
    assert content.get("message", None) == f"A user with email '{email}' already exists."
    assert not content.get("data", True)
    assert content.get("error_code", None) == "USER_ALREADY_EXISTS"
