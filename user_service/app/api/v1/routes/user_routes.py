import uuid

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from app.schemas.user import (
    CreateUserRequest,
    UserSchema,
    UpdateUserRequest,
    UpdateUserPatchRequest,
    Response, RentalSchema
)
from app.common.db import get_session
from app.api.v1 import controllers

router = APIRouter(prefix="/user")


@router.get("/{user_id}")
async def get_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
) -> Response:
    cur_user = await controllers.get_user(session, user_id)

    return Response(
        success=True,
        message="User fetched successfully.",
        data= UserSchema.model_validate(cur_user)
    )


@router.put("/{user_id}")
async def update_user(
        user_id: uuid.UUID,
        user: UpdateUserRequest,
        session: AsyncSession = Depends(get_session)
)-> Response:
    updated_user = await controllers.update_user(session, user_id, user)
    return Response(
        success=True,
        message="User updated successfully",
        data=UserSchema.model_validate(updated_user)
    )


@router.patch("/{user_id}")
async def update_user_patch(
        user_id: uuid.UUID,
        user: UpdateUserPatchRequest,
        session: AsyncSession = Depends(get_session)
) -> Response :

    updated_user = await controllers.update_user_patch(session, user_id, user)

    return Response(
        success=True,
        message="User updated successfully",
        data=UserSchema.model_validate(updated_user)
    )


@router.delete("/{user_id}")
async def delete_user(
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
) -> Response:
    deleted_user = await controllers.delete_user(session, user_id)

    return Response(
        success=True,
        message="User deleted successfully"
    )

@router.post("/{user_id}/rent/{copies}/{book_id}")
async def rent_book(
        user_id: uuid.UUID,
        book_id: uuid.UUID,
        copies: int,
        session: AsyncSession = Depends(get_session)
) -> Response:

    result = await controllers.rent_book(session, user_id, book_id, copies)

    return Response(
        success=True,
        message="Book rented successfully",
        data=RentalSchema.model_validate({"user_id" : user_id, "book_id" : book_id})
    )

@router.post("/{user_id}/return/{copies}/{book_id}")
async def rent_book(
        user_id: uuid.UUID,
        book_id: uuid.UUID,
        copies: int,
        session: AsyncSession = Depends(get_session)
) -> Response:

    result = await controllers.return_book(session, user_id, book_id, copies)

    return Response(
        success=True,
        message="Book returned successfully",
        data=UserSchema.model_validate(result)
    )











