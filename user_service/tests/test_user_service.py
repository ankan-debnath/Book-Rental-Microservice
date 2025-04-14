import uuid

import pytest

from .conftest import client, get_book_id
from .conftest import PORT
from unittest import mock

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
            "name": "demo",
            "email": "demo@example.com",
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
    assert data.get("name", None) == 'demo'
    assert data.get("email", None) == 'demo@example.com'

@mock.patch("app.api.v1.controllers.rent_book.httpx.AsyncClient.patch")
def test_user_rent_post(mock_book_rental_response, get_book_id):
    token_response = client.post(
        url="/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "demo@example.com",
            "password": "new_demo_password"
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

    demo_book_id = get_book_id

    #getting the response
    user_response = client.post(
        f"/v1/user/me/rent/2/{demo_book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    content = user_response.json()
    data = content.get("data", {})


    assert user_response.status_code == 200
    assert content.get("success", False)
    assert content.get("message", None) == 'Book rented successfully'
    assert len(data.get("user_id", "")) == 36
    assert data.get("book_id", "") == demo_book_id


@mock.patch("app.api.v1.controllers.return_book.httpx.AsyncClient.patch")
def test_user_return_post(mock_book_return_response, get_book_id):
    token_response = client.post(
        url="/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "username": "demo@example.com",
            "password": "new_demo_password"
        }
    )
    assert token_response.status_code == 200
    access_token = token_response.json()["access_token"]

    # print(access_token)

    mock_response = mock.Mock(status_code=200)
    mock_response.json.return_value = {"success": True, "message": "Book returned successfully"}
    mock_response.raise_for_status.return_value = None

    mock_book_return_response.return_value = mock_response

    demo_book_id = get_book_id

    # getting the response
    user_response = client.post(
        f"/v1/user/me/return/2/{demo_book_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    content = user_response.json()
    data = content.get("data", {})

    assert user_response.status_code == 200
    assert content.get("success", False)
    assert content.get("message", None) == 'Book returned successfully'
    assert len(data.get("user_id", "")) == 36
    assert data.get("book_id", "") == demo_book_id


