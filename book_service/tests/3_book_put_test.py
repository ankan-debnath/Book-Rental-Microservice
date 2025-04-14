import pytest

from app.common.settings import settings
from .conftest import client, get_book


def test_book_put(get_book):
    response = client.put(
        f"/v1/books/{get_book.book_id}",
        json={
            "name": "The Pragmatic Programmer",
            "author": "Andy Hunt",
            "genre": "Programming",
            "available_copies": 5
        },
        headers={ "Service-Token": settings.SERVICE_KEY }
    )
    assert response.status_code == 200

    content = response.json()
    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'Details updated successfully'
    assert data.get("name", "") == 'The Pragmatic Programmer'
    assert data.get("author", "") == 'Andy Hunt'
    assert data.get("genre", "") == 'Programming'
    assert data.get("available_copies", "") == 5
    assert data.get("book_id", "") == get_book.book_id


@pytest.mark.parametrize(
    "input",
    [
        { "name": "The Pragmatic Programmer", "author": "Andy Hunt" },
        { "name": "The Pragmatic Programmer","genre": "Programming" },
        { "name": "The Pragmatic Programmer" }
    ],
    ids=[ "test1", "test2", "test3"]
)
def test_book_invalid_put(input):
    response = client.post(
        "/v1/books",
        json={**input},
        headers={"Service-Token": settings.SERVICE_KEY}
    )
    assert response.status_code == 422

    content = response.json()


