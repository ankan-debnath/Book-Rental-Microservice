import pytest

from .conftest import client, get_book_id


@pytest.mark.parametrize(
    "token, output",
    [
        (None, "Not authenticated"),
        ("invalid_token", "Could not validate credentials")
    ],
    ids=["without_token", "invalid_token"]
)
def test_patch_route_authentication(get_book_id, token, output):
    user_response = client.delete(
        f"/v1/user/me",
        headers={"Authorization": f"Bearer {token}"} if token else None
    )

    assert user_response.status_code == 401
    content = user_response.json()

    assert content.get("detail", "") == output



def test_user_delete():
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


    user_response = client.delete(
        f"/v1/user/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert user_response.status_code == 200

    content = user_response.json()
    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'User deleted successfully'
    assert not data
