from .conftest import client, get_book_id
from app.api.main import PORT

def test_book_post():
    response = client.post(
        "/v1/books",
        json={
          "name": "The Pragmatic Programmer",
          "author": "Andy Hunt",
          "genre": "Programming",
          "available_copies": 5
        }
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

def test_book_get(get_book_id):
    response = client.get(
        f"/v1/books/{get_book_id}"
    )
    assert response.status_code == 200

    content = response.json()
    data = content.get("data", {})

    assert content.get("success", False)
    assert content.get("message", None) == 'Book fetched successfully.'
    assert data.get("name", "") == 'Test Book'
    assert data.get("author", "") == 'Jane Doe'
    assert data.get("genre", "") == 'Sci-Fi'
    assert data.get("available_copies", "") == 5
    assert data.get("book_id", "") == get_book_id
