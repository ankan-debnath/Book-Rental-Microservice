import sqlite3
import uuid
from collections.abc import Sequence
from fastapi import HTTPException
from starlette import status

from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from app.exceptions.custom_exceptions import BookNotFoundException
from app.models.book_model import BookModel
from app.models import book_model


async def get_books_list(db: AsyncSession, book_ids: list[uuid.UUID]) -> list[BookModel] | None:
    try:
        books = await book_model.get_books_with_ids(db, book_ids)
        return books
    except sqlite3.OperationalError:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Book service not available"
        )

