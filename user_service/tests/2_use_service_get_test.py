import pytest

from .conftest import client

@pytest.mark.parametrize(
    "token, output",
    [
        (None, "Not authenticated"),
        ("invalid_token", "Could not validate credentials")
    ],
    ids=["without_token", "invalid_token"]
)
def test_get_route_authentication(token, output):
    user_response = client.get(
        "/v1/user/me",
        headers={
            "Authorization": f"Bearer {token}"
        } if token else None
    )
    assert user_response.status_code == 401
    content = user_response.json()

    assert content.get("detail", "") == output

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
    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == "User fetched successfully."
    assert len(data.get("user_id", "")) == 36
    assert data.get("name", None) == "demo_user"
    assert data.get("email", None) == "demo@example.com"

@pytest.mark.parametrize(
    "username, password",
    [
        ("invalid_user@example.com", "invalid_password"),
        ("demo@example.com", "invalid_password"),
        ("invalid_user@example.com", "demo_password"),
    ],
    ids=["invalid_user", "valid_user/invalid_password", "invalid_user/valid_password"]
)
def test_unauthorized_user(username, password):
    token_response = client.post(
        url="/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": username,
            "password": password
        }
    )

    assert token_response.status_code == 401

    content = token_response.json()

    data = content.get("detail", {})

    assert data.get('success', True) == False
    assert data.get('message', "") == 'Could not validate credentials'

