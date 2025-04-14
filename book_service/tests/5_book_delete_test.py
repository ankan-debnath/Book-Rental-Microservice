import uuid

import pytest

from .conftest import client, get_book


def test_book_delete(get_book):
    response = client.delete(
        f"/v1/books/{get_book.book_id}"
    )
    assert response.status_code == 200

    content = response.json()

    assert content.get("success", False)
    assert content.get("message", None) == 'Book deleted successfully'
    assert not content.get("data", True)

def test_invalid_book_delete(get_book):
    response = client.delete(
        f"/v1/books/{uuid.uuid4()}"
    )

    assert response.status_code == 404