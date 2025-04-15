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
python -m  app.api.main
```

#### Book Service
```bash
cd book_service
uv venv .venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
uv pip install -e .  
python -m  app.api.main
```


---

## 🧩 User & Rental Service Endpoints

### base url : http://127.0.0.1:5000

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

