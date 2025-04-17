import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import BookNotFoundException
from app.models.book_model import BookModel
from app.models import book_model


async def get_book(db: AsyncSession, book_id: uuid.UUID) -> BookModel | None:

    book = await book_model.get_book(db, book_id)

    if not book:
        raise BookNotFoundException(book_id)

    return book