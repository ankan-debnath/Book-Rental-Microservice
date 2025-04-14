import pytest

from app.common.settings import settings
from .conftest import client, get_book


@pytest.mark.parametrize(
    "input",
    [
        {"name": "Updated Book Title"},  # Single field
        {"author": "Updated Author", "genre": "Fantasy"},  # Two fields
        {"name": "Combo Update", "available_copies": 7, "genre": "Thriller"}  # Three fields
    ],
    ids=["single_field", "double_fields", "three_fields"]
)
def test_book_patch(get_book, input):
    response = client.patch(
        f"/v1/books/{get_book.book_id}",
        json={ **input },
        headers={"Service-Token": settings.SERVICE_KEY}
    )
    assert response.status_code == 200

    content = response.json()
    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'Details updated successfully'
    assert data.get("name", "") == input.get("name", get_book.name)
    assert data.get("author", "") == input.get("author", get_book.author)
    assert data.get("genre", "") == input.get("genre", get_book.genre)
    assert data.get("available_copies", "") == input.get("available_copies", get_book.available_copies)
    assert data.get("book_id", "") == get_book.book_id


def test_book_invalid_patch(get_book):
    response = client.patch(
        f"/v1/books/{get_book.book_id}",
        json={},
        headers={"Service-Token": settings.SERVICE_KEY}
    )
    assert response.status_code == 400

    content = response.json()

    assert not content.get("success", True)
    assert content.get("message", "") == 'No data available to update'
    assert not content.get("data", True)
    assert content.get("error_code", "") == 'NOT_DATA_UPDATE'


@pytest.mark.parametrize(
    "input",
    [ -10, 0 ],
    ids=["negative availability test", "zero availability test"]
)
def test_book_invalid_patch_negative_availability(get_book, input):
    response = client.patch(
        f"/v1/books/{get_book.book_id}",
        json={ "available_copies" : input },
        headers={"Service-Token": settings.SERVICE_KEY}
    )

    assert response.status_code == 409

    content = response.json()

    assert not content.get("success", True)
    assert content.get("message", "") == 'Book availability can not be negative'
    assert not content.get("data", True)
    assert content.get("error_code", "") == 'NEGATIVE_BOOK_AVAILABILITY'


@pytest.mark.parametrize(
    "input",
    [
        {"publisher": "Unknown House"},
        {"price": 20},
        { "random_field": "oops"}
    ],
    ids=[("invalid_case" + str(i+1)) for i in range(3) ]
)
def test_book_patch_bad_request(get_book, input):
    response = client.patch(
        f"/v1/books/{get_book.book_id}",
        json=input,
        headers={"Service-Token": settings.SERVICE_KEY}
    )

    assert response.status_code == 400
