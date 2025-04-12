import uuid

from fastapi import APIRouter, Depends
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession


from app.schemas.books_schema import CreateBookRequest, Response
from app.common.db import get_session
from app.api.v1 import controllers
from app.schemas.books_schema import BookSchema

router = APIRouter(prefix="/books")

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_book(
        request: CreateBookRequest,
        session: AsyncSession = Depends(get_session)
) -> Response:
    book = await controllers.create_book(session, request)
    return Response(
        success=True,
        message="Book added successfully.",
        data=BookSchema.model_validate(book)
    )

@router.get("/{book_id}")
async def get_book(
        book_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
) -> Response:
    book = await controllers.get_book(session, book_id)

    return Response(
        success=True,
        message="Book fetched successfully.",
        data=BookSchema.model_validate(book)
    )