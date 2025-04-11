import uuid

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_fallback
from starlette.status import HTTP_201_CREATED

from app.models import UserModel
from app.schemas.base import BaseSchema
from app.schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    GetUserRequest,
    GetUserResponse,
    UserSchema,
    UpdateUserRequest,
    UpdateUserResponse,
    UpdateUserPatchRequest,
)
from app.common.db import get_session
from app.api.v1 import controllers

router = APIRouter(prefix="/user")

@router.post("", status_code=HTTP_201_CREATED)
async def create_user(
        user: CreateUserRequest,
        session:AsyncSession =  Depends(get_session)
) -> CreateUserResponse:

    new_user = await controllers.add_user(session, user)
    return CreateUserResponse(
        success=True,
        message="User created successfully",
        data=UserSchema.model_validate(new_user)
    )

@router.get("/{user_id}")
async def get_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
) -> GetUserResponse:
    cur_user = await controllers.get_user(session, user_id)

    return GetUserResponse(
        success=True,
        message="User fetched successfully.",
        data= UserSchema.model_validate(cur_user)
    )


@router.put("/{user_id}")
async def update_user(
        user_id: uuid.UUID,
        user: UpdateUserRequest,
        session: AsyncSession = Depends(get_session)
)-> UpdateUserResponse:
    updated_user = await controllers.update_user(session, user_id, user)

    return UpdateUserResponse(
        data=UserSchema.model_validate(updated_user)
    )


@router.patch("/{user_id}")
async def update_user_patch(
        user_id: uuid.UUID,
        user: UpdateUserPatchRequest,
        session: AsyncSession = Depends(get_session)
) -> UpdateUserResponse :

    updated_user = await controllers.update_user_patch(session, user_id, user)

    return UpdateUserResponse(
        data=UserSchema.model_validate(updated_user)
    )













