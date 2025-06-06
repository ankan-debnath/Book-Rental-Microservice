import uuid
from typing import Optional, Any

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseSchema

class Response(BaseSchema):
    success: bool
    message: str
    data: Optional[Any] = None

class UserSchema(BaseSchema):
    user_id: str
    name: str = Field(min_length=1, max_length=30)
    email: EmailStr

class CreateUserRequest(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str


class UpdateUserRequest(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str

class UpdateUserPatchRequest(BaseSchema):
    name: Optional[str] = Field(min_length=1, max_length=100, default=None)
    email: Optional[EmailStr] = Field(default=None)
    password: Optional[str] = Field(default=None)


class GetUserRequest(BaseSchema):
    user_id: uuid.UUID = Field(min_length=36, max_length=36)

class RentalSchema(BaseSchema):
    user_id: str
    book_id: uuid.UUID

class ErrorResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: str

class Token(BaseModel):
    access_token: str
    grant_type: str

class TokenData(BaseModel):
    user_id: str | None = None

class BookSchema(BaseSchema):
    book_id: uuid.UUID
    name: str = Field(min_length=1, max_length=100)
    author: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=50)
    available_copies: int

class RentalResponseSchema(BaseSchema):
    id: int
    book_id: str



