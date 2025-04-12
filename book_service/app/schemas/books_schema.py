import uuid
from typing import Optional, Any
from pydantic import Field, BaseModel


from .base import BaseSchema


class Response(BaseSchema):
    success: bool
    message: str
    data: Optional[Any] = None


class CreateBookRequest(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=50)
    available_copies: int = 0

class BookSchema(CreateBookRequest):
    book_id: uuid.UUID


class ErrorResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: str
