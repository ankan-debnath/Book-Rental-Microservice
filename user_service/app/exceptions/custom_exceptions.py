import uuid

from app.exceptions.base import CustomException
from fastapi import status

class UserAlreadyExistsException(CustomException):
    error_code: str = "USER_ALREADY_EXISTS"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, email, **kwargs):
        self.message = f"A user with email '{email}' already exists."
        self.data = {"email": email}

class UserNotFoundException(CustomException):
    error_code="USER_NOT_FOUND"
    status_code=status.HTTP_404_NOT_FOUND

    def __init__(self, user_id: uuid.UUID):
        self.message = "User not found."
        self.data = {"user_id": user_id}

class NoDataToUpdateException(CustomException):
    error_code: str = "NOT_DATA_UPDATE"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        self.message = "No data available to update"


class BookNotFoundException(CustomException):
    error_code: str = "BOOK_NOT_FOUND"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, book_id: uuid.UUID, **kwargs):
        self.message = f"No book found with id {book_id}"
        self.data = {"email": book_id}

class BookNotAvailableException(CustomException):
    error_code: str = "ENOUGH_COPIES_NOT_AVAILABLE"
    status_code: int = status.HTTP_409_CONFLICT

    def __init__(self, book_id: uuid.UUID, **kwargs):
        self.message = f"Book is currently not available for rent"
        self.data = {"book_id": book_id}

class BookServiceException(CustomException):
    def __init__(self, message: str):
        self.message = message

class UserServiceException(CustomException):
    def __init__(self, message: str):
        self.message = message


class InvalidRentalReturnException(CustomException):
    error_code: str = "FAILED_TO_RETURN"
    status_code: int = status.HTTP_409_CONFLICT

    def __init__(self, book_id: uuid.UUID, message):
        self.message = message
        self.data = {"book": book_id}

