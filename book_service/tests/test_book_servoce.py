from .conftest import client
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