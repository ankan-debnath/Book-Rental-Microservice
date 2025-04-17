import pytest

from app.common.settings import settings
from .conftest import client, get_book

def test_book_post():
    response = client.post(
        "/v1/books",
        json={
            "name": "The Pragmatic Programmer",
            "author": "Andy Hunt",
            "genre": "Programming",
            "available_copies" : 5
        },
        headers={ "Service-Token": settings.SERVICE_KEY }
    )
    assert response.status_code == 201

    content = response.json()
    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'Book added successfully.'
    assert data.get("name", "") == 'The Pragmatic Programmer'
    assert data.get("author", "") == 'Andy Hunt'
    assert data.get("genre", "") ==  'Programming'
    assert data.get("available_copies", "") ==  5
    assert len(data.get("book_id", "")) ==  36


@pytest.mark.parametrize(
    "input",
    [
        { "name": "The Pragmatic Programmer", "author": "Andy Hunt" },
        { "name": "The Pragmatic Programmer","genre": "Programming" },
        { "name": "The Pragmatic Programmer" }
    ],
    ids=[ "test1", "test2", "test3"]
)
def test_book_invalid_post(input):
    response = client.post(
        "/v1/books",
        json={ **input },
        headers={ "Service-Token": settings.SERVICE_KEY }
    )
    assert response.status_code == 422

    content = response.json()
