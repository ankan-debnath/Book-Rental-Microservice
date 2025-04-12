import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BookModel
from app.exceptions.custom_exceptions import BookNotFoundException, NegativeAvailabilityException
from app.models import book_model

async def update_book_availability(db: AsyncSession, book_id: uuid.UUID, copies:int)-> BookModel:

    book = await book_model.update_availability(db, book_id, copies)

    if book == 0:
        raise BookNotFoundException(book_id)

    if book == -1:
        raise NegativeAvailabilityException(book_id)

    return book