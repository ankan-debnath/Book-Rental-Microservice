import uuid
from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import BookNotFoundException
from app.models.book_model import BookModel
from app.models import book_model


async def get_all_books(db: AsyncSession) -> Sequence[BookModel]:

    book = await book_model.get_all_books(db)

    return book