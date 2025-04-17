import random
import uuid

import pytest

from app.common.settings import settings
from .conftest import client, get_book
from app.api.main import PORT


def test_book_get(get_book):
    response = client.get(
        f"/v1/books/{get_book.book_id}",
        headers={ "Service-Token": settings.SERVICE_KEY }
    )
    assert response.status_code == 200

    content = response.json()
    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'Book fetched successfully.'
    assert data.get("name", "") == get_book.name
    assert data.get("author", "") == get_book.author
    assert data.get("genre", "") == get_book.genre
    assert data.get("available_copies", "") == get_book.available_copies
    assert data.get("book_id", "") == get_book.book_id



@pytest.mark.parametrize(
    "book_id, status_code",
    [ (uuid.uuid4(), 404), ("123456789910", 422) ],
    ids=["test1", "test2"]
)
def test_book_invalid_get(book_id, status_code):
    response = client.get(
        f"/v1/books/{book_id}",
        headers={ "Service-Token": settings.SERVICE_KEY }
    )
    assert response.status_code == status_code


