import pytest

from .conftest import client, get_book_id
from unittest import mock

@pytest.mark.parametrize(
    "token, output",
    [
        (None, "Not authenticated"),
        ("invalid_token", "Could not validate credentials")
    ],
    ids=["without_token", "invalid_token"]
)
def test_patch_route_authentication(get_book_id, token, output):
    user_response = client.post(
        f"/v1/user/me/rent/2/{get_book_id}",
        headers={"Authorization": f"Bearer {token}"} if token else None
    )

    assert user_response.status_code == 401
    content = user_response.json()

    assert content.get("detail", "") == output

@pytest.mark.parametrize(
    "token, output",
    [
        (None, "Not authenticated"),
        ("invalid_token", "Could not validate credentials")
    ],
    ids=["without_token", "invalid_token"]
)
def test_patch_route_authentication(get_book_id, token, output):
    user_response = client.post(
        f"/v1/user/me/return/2/{get_book_id}",
        headers={"Authorization": f"Bearer {token}"} if token else None
    )

    assert user_response.status_code == 401
    content = user_response.json()

    assert content.get("detail", "") == output



@pytest.mark.parametrize(
    "copies", [0, -2], ids=["zero_copies_rent", "negative_copies_rent"]
)
def test_user_rent_invalid_copies(get_book_id, copies):
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

    user_response = client.post(
        f"/v1/user/me/rent/{copies}/{get_book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert user_response.status_code == 422

    content = user_response.json()
    data = content.get("detail", {})

    assert not data.get("success", True)
    assert data.get("message", "") ==  'No. of copies must be positive'


@mock.patch("app.api.v1.controllers.rent_book.httpx.AsyncClient.patch")
def test_user_rent_post(mock_book_rental_response, get_book_id):
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

    # print(access_token)

    #mocking external api call
    mock_response = mock.Mock(status_code=200)
    mock_response.json.return_value= { "success": True, "message": "Book rented successfully"}
    mock_response.raise_for_status.return_value = None

    mock_book_rental_response.return_value = mock_response


    #getting the response
    user_response = client.post(
        f"/v1/user/me/rent/2/{get_book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    content = user_response.json()
    data = content.get("data", {})


    assert user_response.status_code == 200
    assert content.get("success", False)
    assert content.get("message", None) == 'Book rented successfully'
    assert len(data.get("user_id", "")) == 36
    assert data.get("book_id", "") == get_book_id



@pytest.mark.parametrize(
    "copies", [0, -2], ids=["zero_copies_rent", "negative_copies_rent"]
)
def test_user_return_invalid_copies(get_book_id, copies):
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

    user_response = client.post(
        f"/v1/user/me/return/{copies}/{get_book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert user_response.status_code == 422

    content = user_response.json()
    data = content.get("detail", {})

    assert not data.get("success", True)
    assert data.get("message", "") ==  'No. of copies must be positive'


@pytest.mark.parametrize(
    "copies",
    [ 4, 5],
    ids=["excess_return1", "excess_return2"]
)
def test_user_return_excess(get_book_id, copies):
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

    user_response = client.post(
        f"/v1/user/me/return/{copies}/{get_book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert user_response.status_code == 409

    content = user_response.json()

    assert not content.get("success", True)
    assert content.get("message") == f'attempting to return {copies} copies but only 2 were rented.'
    assert not content.get("data", True)
    assert content.get("error_code", "") == 'FAILED_TO_RETURN'


@mock.patch("app.api.v1.controllers.return_book.httpx.AsyncClient.patch")
def test_user_return_post(mock_book_return_response, get_book_id):
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

    mock_response = mock.Mock(status_code=200)
    mock_response.json.return_value = {"success": True, "message": "Book returned successfully"}
    mock_response.raise_for_status.return_value = None

    mock_book_return_response.return_value = mock_response


    # getting the response
    user_response = client.post(
        f"/v1/user/me/return/2/{get_book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    content = user_response.json()
    data = content.get("data", {})

    assert user_response.status_code == 200
    assert content.get("success", False)
    assert content.get("message", None) == 'Book returned successfully'
    assert len(data.get("user_id", "")) == 36
    assert data.get("book_id", "") == get_book_id
