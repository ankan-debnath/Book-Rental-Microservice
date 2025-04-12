import uuid

from starlette import status

from app.exceptions.base import CustomException


class BookNotFoundException(CustomException):
    error_code: str = "BOOK_NOT_FOUND"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, book_id: uuid.UUID, **kwargs):
        self.message = f"No book found with id {book_id}"
        self.data = {"email": book_id}

class NoDataToUpdateException(CustomException):
    error_code: str = "NOT_DATA_UPDATE"
    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self):
        self.message = "No data available to update"

