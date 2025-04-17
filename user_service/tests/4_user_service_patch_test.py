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
def test_patch_route_authentication(token, output):
    user_response = client.patch(
        "/v1/user/me",
        headers={
            "Authorization": f"Bearer {token}"
        } if token else None,
        json={
            "name": "new_demo",
            "email": "new_demo@example.com"
        }
    )
    assert user_response.status_code == 401
    content = user_response.json()

    assert content.get("detail", "") == output


@pytest.mark.parametrize(
    "input, output",
    [
        (
                {"invalid_name": "updated_name", "invalid_password": "supersecret"},
                { "status_code" : 400, "message" : 'No data available to update', 'data': None, 'error_code': 'NOT_DATA_UPDATE'}
        ),
        (None, {"status_code" : 422 })
    ],
    ids=["invalid_credentials", "no_credentials"]
)
def test_patch_invalid_cred(input, output):
    token_response = client.post(
        url="/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "new_demo@example.com",
            "password": "new_demo_password"
        }
    )

    assert token_response.status_code == 200
    access_token = token_response.json()["access_token"]

    user_response = client.patch(
        "/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json=input
    )

    content = user_response.json()

    for key, val in content.items():
        if key in output:
            assert content[key] == output[key]


def test_user_patch():
    token_response = client.post(
        url="/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "new_demo@example.com",
            "password": "new_demo_password"
        }
    )

    assert token_response.status_code == 200
    access_token = token_response.json()["access_token"]

    user_response = client.patch(
        "/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={
            "email": "demo@example.com",
            "password": "demo_password",
        }
    )

    content = user_response.json()
    data = content.get("data", {})

    assert user_response.status_code == 200
    content = user_response.json()
    data = content.get("data", None)

    assert content.get("success", False)
    assert content.get("message", None) == 'User updated successfully'
    assert len(data.get("user_id", "")) == 36
    assert data.get("name", None) == 'new_demo'
    assert data.get("email", None) == 'demo@example.com'



