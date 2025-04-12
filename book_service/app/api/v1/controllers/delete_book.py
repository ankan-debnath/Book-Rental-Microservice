import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import BookModel
from app.exceptions.custom_exceptions import BookNotFoundException
from app.models import book_model

async def delete_book(db: AsyncSession, book_id: uuid.UUID)-> BookModel:
    book = await book_model.delete_book(db, book_id)

    if not book:
        raise BookNotFoundException(book_id)

    return book