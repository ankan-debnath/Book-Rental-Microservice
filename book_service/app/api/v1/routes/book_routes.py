import uuid

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import NegativeAvailabilityException
from app.schemas.books_schema import (
    CreateBookRequest,
    UpdateBookRequest,
    Response, BookListRequest
)
from app.common.db import get_session
from app.api.v1 import controllers
from app.schemas.books_schema import BookSchema
from app.auth.dependencies import verify_token

router = APIRouter(prefix="/books")

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(
        request: CreateBookRequest,
        authorize:bool = Depends(verify_token),
        session: AsyncSession = Depends(get_session)
) -> Response:
    book = await controllers.create_book(session, request)
    return Response(
        success=True,
        message="Book added successfully.",
        data=BookSchema.model_validate(book)
    )


@router.get("/all")
async def get_all_books(
        authorize:bool = Depends(verify_token),
        session: AsyncSession = Depends(get_session)
):
    books = await controllers.get_all_books(session)

    return Response(
        success=True,
        message="Books fetched successfully.",
        data=[BookSchema.model_validate(book) for book in books]
    )


@router.post("/list")
async def get_books_list(
        request: BookListRequest,
        # authorize:bool = Depends(verify_token),
        session: AsyncSession = Depends(get_session)
):
    books = await controllers.get_books_list(session, request.book_ids)

    return Response(
        success=True,
        message="Books fetched successfully.",
        data=[BookSchema.model_validate(book) for book in books]
    )



@router.get("/{book_id}")
async def get_book(
        book_id: uuid.UUID,
        authorize:bool = Depends(verify_token),
        session: AsyncSession = Depends(get_session)
) -> Response:
    book = await controllers.get_book(session, book_id)

    return Response(
        success=True,
        message="Book fetched successfully.",
        data=BookSchema.model_validate(book)
    )
@router.delete("/{book_id}")
async def delete_book(
        book_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
) -> Response:
    book = await controllers.delete_book(session, book_id)

    return Response(
        success=True,
        message="Book deleted successfully"
    )


@router.put("/{book_id}")
async def update_book(
        book_id: uuid.UUID,
        request: CreateBookRequest,
        authorize:bool = Depends(verify_token),
        session: AsyncSession = Depends(get_session)
) -> Response:
    updated_book = await controllers.update_book(session, book_id, request)

    return Response(
        success=True,
        message="Details updated successfully",
        data=BookSchema.model_validate(updated_book)
    )


@router.patch("/{book_id}")
async def update_book(
        book_id: uuid.UUID,
        request: UpdateBookRequest,
        authorize:bool = Depends(verify_token),
        session: AsyncSession = Depends(get_session)
) -> Response:
    updated_book = await controllers.update_book(session, book_id, request)

    return Response(
        success=True,
        message="Details updated successfully",
        data=BookSchema.model_validate(updated_book)
    )

@router.patch("/rent/{copies}/{book_id}")
async def rent_book(
        book_id: uuid.UUID,
        copies:int,
        authorize: bool = Depends(verify_token),
        session: AsyncSession = Depends(get_session)
) -> Response:

    if copies <= 0:
        raise NegativeAvailabilityException(book_id)

    result = await controllers.update_book_availability(session, book_id, -copies)

    return Response(
        success=True,
        message="Book rented successfully",
        data=BookSchema.model_validate(result)
    )

@router.patch("/return/{copies}/{book_id}")
async def return_book(
        book_id: uuid.UUID,
        copies:int,
        authorize:bool = Depends(verify_token),
        session: AsyncSession = Depends(get_session)
) -> Response:

    if copies <= 0:
        raise NegativeAvailabilityException(book_id)

    result = await controllers.update_book_availability(session, book_id, copies)

    return Response(
        success=True,
        message="Book returned successfully",
        data=BookSchema.model_validate(result)
    )

