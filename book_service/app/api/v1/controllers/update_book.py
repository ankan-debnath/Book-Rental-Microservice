import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import BookNotFoundException
from app.schemas.books_schema import CreateBookRequest
from app.models import book_model, BookModel



async def update_book(db: AsyncSession, book_id: uuid.UUID,
                      request: CreateBookRequest) -> BookModel:

    update_details = request.model_dump(exclude_unset=True)
    # print(book_id)
    # print(update_details)
    #
    updated_book = await book_model.update_book(db, book_id, update_details)

    if not updated_book:
        raise BookNotFoundException(book_id)

    return updated_book