import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import (
    BookNotFoundException,
    NoDataToUpdateException,
    NegativeAvailabilityException
)
from app.schemas.books_schema import BookRequest
from app.models import book_model, BookModel


async def update_book(db: AsyncSession, book_id: uuid.UUID,
                      request: BookRequest) -> BookModel:

    update_details = request.model_dump(exclude_unset=True)

    if not update_details:
        raise NoDataToUpdateException

    updated_book = await book_model.update_book(db, book_id, update_details)

    if updated_book == 0:
        raise BookNotFoundException(book_id)

    if updated_book == -1:
        raise NegativeAvailabilityException(book_id)

    return updated_book