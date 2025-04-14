import pytest

from app.common.settings import settings
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

def test_book_rent(get_book):
    copies_to_rent = 2          # test_book has 5 copies
    response = client.patch(
        f"/v1/books/rent/{copies_to_rent}/{get_book.book_id}",
        headers={
            "Service-Token": settings.SERVICE_KEY
        }
    )

    assert response.status_code == 200

    content = response.json()

    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'Book rented successfully'
    assert data.get("name", "") == get_book.name
    assert data.get("author", "") == get_book.author
    assert data.get("genre", "") == get_book.genre
    assert data.get("available_copies", "") == (get_book.available_copies - copies_to_rent)
    assert data.get("book_id", "") == get_book.book_id

def test_book_return(get_book):
    copies_to_return = 2  # test_book has 5 copies
    response = client.patch(
        f"/v1/books/return/{copies_to_return}/{get_book.book_id}",
        headers={
            "Service-Token": settings.SERVICE_KEY
        }
    )

    assert response.status_code == 200

    content = response.json()

    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'Book returned successfully'
    assert data.get("name", "") == get_book.name
    assert data.get("author", "") == get_book.author
    assert data.get("genre", "") == get_book.genre
    assert data.get("available_copies", "") == (get_book.available_copies + copies_to_return)
    assert data.get("book_id", "") == get_book.book_id
