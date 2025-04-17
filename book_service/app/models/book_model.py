import sqlite3
import uuid
from collections.abc import Sequence

from sqlalchemy import String, CheckConstraint
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import BookNotFoundException
from app.models.base import ORMBase


class BookModel(ORMBase):
    __tablename__ = "books"

    book_id: Mapped[uuid.UUID] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    available_copies: Mapped[int] = mapped_column(nullable=False, default=0)

    __table_args__ = (
        CheckConstraint('available_copies >= 0', name='check_price_non_negative'),
    )
    __mapper_args__ = {
        "confirm_deleted_rows": False
    }

async def create_book(db: AsyncSession, book_details: dict) -> BookModel:
    statement = (
        insert(BookModel)
        .values(**book_details)
        .returning(BookModel)
    )

    try:
        result = await db.execute(statement)
        user = result.scalars().first()

        await db.commit()
        await db.refresh(user)
    except sqlite3.OperationalError:
        await db.rollback()
        raise

    return user

async def get_book(db: AsyncSession, book_id: uuid.UUID) -> BookModel | None:
    statement = (
        select(BookModel)
        .where(BookModel.book_id == str(book_id))
    )

    try:
        result = await db.execute(statement)
        user =  result.scalars().first()

        if not user:
            return None
        await db.commit()
        await db.refresh(user)
    except sqlite3.OperationalError:
        await db.rollback()
        raise

    return user

async def delete_book(db: AsyncSession, book_id: uuid.UUID) -> BookModel | None:
    statement = (
        delete(BookModel)
        .where(BookModel.book_id == str(book_id))
        .returning(BookModel)
    )

    try:
        result = await db.execute(statement)
        book = result.scalars().first()
        if not book:
            return None
        await db.commit()
    except sqlite3.OperationalError:
        await db.rollback()
        raise

    return book

async def update_book(db: AsyncSession, book_id: uuid.UUID,
                      update_details: dict) -> BookModel | int:
    statement = (
        update(BookModel)
        .where(BookModel.book_id == str(book_id))
        .values(**update_details)
        .returning(BookModel)
    )

    try:
        result = await db.execute(statement)
        updated_book = result.scalars().first()
        if not updated_book:
            return 0

        if updated_book.available_copies < 0:
            return -1

        await db.commit()
        await db.refresh(updated_book)
    except sqlite3.OperationalError:
        await db.rollback()
        raise

    return updated_book

async def update_availability(db: AsyncSession, book_id: uuid.UUID, copies:int) -> BookModel | int:
    statement = (
        update(BookModel)
        .where(BookModel.book_id == str(book_id))
        .values(available_copies=BookModel.available_copies + copies)
        .returning(BookModel)
    )

    try:
        result = await db.execute(statement)
        updated_book = result.scalars().first()

        if not updated_book:
            return 0

        if updated_book.available_copies < 0:
            return -1

        await db.commit()
        await db.refresh(updated_book)

    except sqlite3.OperationalError:
        await db.rollback()
        raise

    return updated_book

async def get_all_books(db: AsyncSession) -> Sequence[BookModel]:
    statement = select(BookModel)

    try:
        result = await db.execute(statement)
        book_list = result.scalars().all()

        await db.commit()
        for book in book_list:
            await db.refresh(book)
        return book_list

    except sqlite3.OperationalError:
        await db.rollback()
        raise

async def get_books_with_ids(db: AsyncSession, ids: list[uuid.UUID]) -> list[BookModel]:
    books: list[BookModel] = []
    try:
        for book_id in ids:
            statement = (
                select(BookModel)
                .where(BookModel.book_id == str(book_id))
            )
            result = await db.execute(statement)
            book = result.scalars().first()
            await db.commit()
            if  book:
                books.append(book)

        for book in books:
            await db.refresh(book)


        return books

    except sqlite3.OperationalError:
        await db.rollback()
        raise



