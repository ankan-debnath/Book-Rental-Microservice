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

