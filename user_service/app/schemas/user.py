import uuid
from typing import Optional, Any

from pydantic import BaseModel, EmailStr, Field

from app.schemas.base import BaseSchema

class UserSchema(BaseSchema):
    user_id: uuid.UUID
    name: str = Field(min_length=1, max_length=30)
    email: EmailStr

class CreateUserRequest(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

class Response(BaseSchema):
    success: bool
    message: str
    data: Optional[Any] = None

class CreateUserResponse(Response):
    pass

class UpdateUserRequest(BaseSchema):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

class UpdateUserPatchRequest(BaseSchema):
    name: Optional[str] = Field(min_length=1, max_length=100, default=None)
    email: Optional[EmailStr] = Field(default=None)


class GetUserResponse(Response):...

class UpdateUserResponse(Response):
    success: bool = True
    message: str = "User updated successfully"

class GetUserRequest(BaseSchema):
    user_id: uuid.UUID = Field(min_length=36, max_length=36)

class ErrorResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None
    error_code: str

