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
def test_put_route_authentication(token, output):
    user_response = client.put(
        "/v1/user/me",
        headers={
            "Authorization": f"Bearer {token}"
        } if token else None,
        json={
            "name": "new_demo",
            "email": "new_demo@example.com",
            "password": "new_demo_password"
        }
    )
    assert user_response.status_code == 401
    content = user_response.json()

    assert content.get("detail", "") == output


def test_user_put_invalid_cred():
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
            "password": "new_demo_password"
        }
    )

    content = user_response.json()
    data = content.get("data", None)

    assert user_response.status_code == 422


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
    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'User updated successfully'
    assert len(data.get("user_id", "")) == 36
    assert data.get("name", None) == 'new_demo'
    assert data.get("email", None) == 'new_demo@example.com'

