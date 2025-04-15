import uuid

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.auth.dependencies import get_current_user
from app.exceptions.custom_exceptions import CredentialsException
from app.models import UserModel
from app.schemas.user import (
    CreateUserRequest,
    UserSchema,
    UpdateUserRequest,
    UpdateUserPatchRequest,
    Response, RentalSchema, BookSchema, RentalResponseSchema
)
from app.common.db import get_session
from app.api.v1 import controllers

router = APIRouter(prefix="/user")


@router.get("/{user_id}")
async def get_user(
        user_id: str,
        user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> Response:

    if user_id == "me":
        user_id = user.user_id

    if str(user.user_id) != str(user_id):
        raise CredentialsException(
            detail={"success" : False, "message": "User is unauthorized"}
        )
    cur_user = await controllers.get_user(session, user_id)

    return Response(
        success=True,
        message="User fetched successfully.",
        data= UserSchema.model_validate(cur_user)
    )


@router.put("/{user_id}")
async def update_user(
        user_id: str,
        user: UpdateUserRequest,
        cur_user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
)-> Response:

    if user_id == "me":
        user_id = cur_user.user_id

    if str(user_id) != str(cur_user.user_id):
        raise CredentialsException(
            detail={"success": False, "message": "User is unauthorized"}
        )
    updated_user = await controllers.update_user(session, user_id, user)

    return Response(
        success=True,
        message="User updated successfully",
        data=UserSchema.model_validate(updated_user)
    )


@router.patch("/{user_id}")
async def update_user_patch(
        user_id: str,
        user: UpdateUserPatchRequest,
        cur_user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> Response :

    if user_id == "me":
        user_id = cur_user.user_id


    if str(user_id) != str(cur_user.user_id):
        raise CredentialsException(
            detail={"success": False, "message": "User is unauthorized"}
        )


    updated_user = await controllers.update_user_patch(session, user_id, user)

    return Response(
        success=True,
        message="User updated successfully",
        data=UserSchema.model_validate(updated_user)
    )


@router.delete("/{user_id}")
async def delete_user(
        user_id: str,
        cur_user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> Response:

    if user_id == "me":
        user_id = cur_user.user_id


    if str(user_id) != str(cur_user.user_id):
        raise CredentialsException(
            detail={"success": False, "message": "User is unauthorized"}
        )

    deleted_user = await controllers.delete_user(session, user_id)

    return Response(
        success=True,
        message="User deleted successfully"
    )

@router.get("/{user_id}/books/all")
async def get_all_books(
        user_id: str,
        cur_user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
):
    if user_id == "me":
        user_id = cur_user.user_id

    if str(user_id) != str(cur_user.user_id):
        raise CredentialsException(
            detail={"success": False, "message": "User is unauthorized"}
        )

    books = await controllers.get_all_books()

    return Response(
        success=True,
        message="Book returned successfully",
        data=[BookSchema.model_validate(book) for book in books]
    )



@router.post("/{user_id}/rent/{copies}/{book_id}")
async def rent_book(
        user_id: str,
        book_id: uuid.UUID,
        copies: int,
        cur_user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> Response:

    if user_id == "me":
        user_id = cur_user.user_id

    if str(user_id) != str(cur_user.user_id):
        raise CredentialsException(
            detail={"success": False, "message": "User is unauthorized"}
        )

    result = await controllers.rent_book(session, user_id, book_id, copies)

    return Response(
        success=True,
        message="Book rented successfully",
        data=RentalSchema.model_validate({"user_id" : user_id, "book_id" : book_id})
    )

@router.post("/{user_id}/return/{copies}/{book_id}")
async def return_book(
        user_id: str,
        copies: int,
        book_id: uuid.UUID,
        cur_user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> Response:

    if user_id == "me":
        user_id = cur_user.user_id

    if str(user_id) != str(cur_user.user_id):
        raise CredentialsException(
            detail={"success": False, "message": "User is unauthorized"}
        )


    result = await controllers.return_book(session, user_id, book_id, copies)

    return Response(
        success=True,
        message="Book returned successfully",
        data=RentalSchema.model_validate({"user_id" : user_id, "book_id" : book_id})
    )


@router.get("/{user_id}/rentals")
async def get_rental_details(
        user_id: str,
        cur_user: UserModel = Depends(get_current_user),
        session: AsyncSession = Depends(get_session)
) -> Response:

    if user_id == "me":
        user_id = cur_user.user_id

    if str(user_id) != str(cur_user.user_id):
        raise CredentialsException(
            detail={"success": False, "message": "User is unauthorized"}
        )

    rentals = await controllers.get_rental_details(session, user_id)
    print(rentals)

    return Response(
        success=True,
        message="Book rented successfully",
        data= rentals
    )






