import uuid
from typing import Optional, Any
from pydantic import Field, BaseModel


from .base import BaseSchema


class Response(BaseSchema):
    success: bool
    message: str
    data: Optional[Any] = None

class BookRequest(BaseSchema):
    name: Optional[str] = Field(min_length=1, max_length=100, default=None)
    author: Optional[str] = Field(min_length=1, max_length=100, default=None)
    genre: Optional[str] = Field(min_length=1, max_length=50, default=None)
    available_copies: Optional[int] = None

class CreateBookRequest(BookRequest):
    name: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=50)
    available_copies: int

class UpdateBookRequest(BookRequest):...

class BookSchema(CreateBookRequest):
    book_id: uuid.UUID


class BookListRequest(BaseSchema):
    book_ids: list[uuid.UUID]


class ErrorResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: str
