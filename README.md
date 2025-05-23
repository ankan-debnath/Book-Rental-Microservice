# 📚 Book Rental Microservice System

This project is a microservice-based Book Rental API system consisting of two separate services:

- **User & Rental Service**
- **Book Service**

Each service runs independently and communicates via REST APIs. This document outlines the API endpoints for the **User & Rental Service**.

---

## 🚀 Getting Started

Each microservice must be run separately. Ensure that both services are up and running for the system to function properly.

### 📥 Clone the Repository

```bash
git clone https://git.epam.com/ankan_debnath/book-rental-microservice.git
cd book-rental-microservice
```

### Prerequisites

- Python 3.9+
- FastAPI / Flask (depending on your service framework)
- Uvicorn (for FastAPI)
- Virtual environment setup
- PostgreSQL / SQLite (as required)

### 🔧 Installation & Running

```bash
pip install uv
```

#### User & Rental Service
```bash
cd user_service
uv venv .venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
uv pip install -e .  
alembic upgrade head
python -m  app.api.main
```
#### .env file format
```doctest
# SQLite database for user service
DB_URL=sqlite+aiosqlite:///db/user.db

# URL of the Book Service (used to fetch book data)
BOOK_SERVICE_URI=http://127.0.0.1:8000/v1/books

# JWT Authentication configuration
SECRET_KEY=super-secret-key              # Secret used for signing JWTs
ALGORITHM=HS256                          # Algorithm used to sign the tokens
ACCESS_TOKEN_EXPIRE_MINUTES=30           # Access token expiry duration

# Application port (used when running the user service locally)
PORT=5000

# Internal API key (used for service-to-service authentication)
API_KEY=secret-key

```

#### Book Service
```bash
cd book_service
uv venv .venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
alembic upgrade head
uv pip install -e .  
python -m  app.api.main
```
#### .env file format
```doctest
# SQLite database for book service
DB_URL=sqlite+aiosqlite:///db/book.db

# Internal API key used for service-to-service authentication
SERVICE_KEY="secret-key"

# Port the Book Service will run on
PORT=8000

```
---

### Final Command to run the app
```commandline
python -m http.server 5500 # runnig frontend at port 5500
```

## 🧩 User & Rental Service Endpoints


### 🔐 Authentication

#### `POST /token`
Create a token for authenticated requests.

- **Request Body**: (e.g., username and password)
- **Response**: JWT token

> ⚠️ All routes except `/`, `/token`, and `/v1/user(POST)` require an **Authorization** header with a Bearer token:
> ```python
> headers = {
>     "Authorization": f"Bearer {token}"
> }
> ```

---

### 👤 User Management

#### `POST /v1/user`
Create a new user.

- **Request Body**:
  ```json
  {
    "username": "string",
    "email": "user@example.com",
    "password": "string"
  }
  ```
- **Response**: Created user data

---

#### `GET /v1/user/{user_id}`
#### `GET /v1/user/me`
Fetch user details by ID.

- **Response**:
  ```json
  {
    "user_id": "2a74775a-f253-41e2-9fd8-b98fff7ad5c7",
    "username": "string",
    "email": "user@example.com"
  }
  ```

---

#### `PUT /v1/user/{user_id}`
#### `PUT /v1/user/me`
Fully update user information.

- **Request Body**:
  ```json
  {
    "username": "new_username",
    "email": "new_email@example.com"
  }
  ```
- **Response**: Updated user data

---

#### `PATCH /v1/user/{user_id}`
#### `PATCH /v1/user/me`
Partially update user information.

- **Request Body**:
  ```json
  {
    "email": "updated_email@example.com"
  }
  ```
- **Response**: Updated fields

---

#### `DELETE /v1/user/{user_id}`
#### `DELETE /v1/user/me`
Delete a user account.

- **Response**: Success message

---

### 📖 Book Rental Operations

---

#### `GET /v1/user/{user_id}/books/all`
Get a list of all books available in the system.

- **Path Params**:
  - `user_id` - User ID or use `"me"` to reference the authenticated user

- **Authorization**: Requires Bearer token in headers

- **Response**:
  ```json
  {
    "success": true,
    "message": "Book returned successfully",
    "data": [
      {
        "book_id": "string",
        "name": "string",
        "author": "string",
        "genre": "string",
        "available_copies": 0
      },
      ...
    ]
  }

---

#### `POST /v1/user/{user_id}/rent/{copies}/{book_id}`
Rent one or more copies of a book.

- **Path Params**:
  - `user_id` - User ID
  - `copies` - Number of copies to rent
  - `book_id` - Book ID
- **Response**: Rental confirmation

---

#### `POST /v1/user/{user_id}/return/{copies}/{book_id}`
Return one or more copies of a previously rented book.

- **Path Params**:
  - `user_id` - User ID
  - `copies` - Number of copies to return
  - `book_id` - Book ID
- **Response**: Return confirmation

---

#### `GET /v1/user/rentals/{user_id}`
Retrieve all rental records associated with a user.

- **Path Params**:
  - `user_id` - User ID or use `"me"` to reference the authenticated user

- **Authorization**: Requires Bearer token in headers

- **Response**:
  ```json
  {
    "success": true,
    "message": "Book rented successfully",
    "data": [
      {
        "id": 5,
        "book_id": "249940aa-4955-4392-b618-a16baa0aaf2a"
      },
      {
        "id": 6,
        "book_id": "249940aa-4955-4392-b618-a16baa0aaf2a"
      }
    ]
  }


### 🏠 Root Endpoint

#### `GET /`
Basic index endpoint to verify the service is running.

---

## 🧪 Testing

Use `curl`, Postman, or Swagger UI (`/docs`) to interact with the API.

---

## 📌 Notes

- Each microservice must be run on a different port.
- Make sure to provide the appropriate base URLs while testing the endpoints.
- JWT tokens are required for secured endpoints if implemented.

---

## 📫 Contact

For issues or contributions, please open an issue or submit a pull request.

