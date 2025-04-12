from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.books_schema import CreateBookRequest
from app.models import book_model

async def create_book(session: AsyncSession, request: CreateBookRequest):
    book_details = request.model_dump()
    user = await book_model.create_book(session, book_details)

    return user