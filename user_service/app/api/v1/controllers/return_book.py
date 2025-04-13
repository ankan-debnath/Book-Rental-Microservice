import sqlite3
import uuid
import httpx

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.settings import settings
from app.exceptions.custom_exceptions import (
    BookNotFoundException,
    BookNotAvailableException,
    BookServiceException,
    UserServiceException, UserNotFoundException,
    InvalidRentalReturnException
)
from app.models import user_model


BOOKS_URI = settings.BOOK_SERVICE_URI

async def return_book(db: AsyncSession, user_id: uuid.UUID, book_id: uuid.UUID, copies:int):
    rentals = await user_model.get_user_rentals(db, user_id)

    cur_book_rentals = 0
    for rental in rentals:
        cur_book_rentals += rental.book_id == str(book_id)

    if cur_book_rentals == 0:
        raise InvalidRentalReturnException(
            book_id=book_id,
            message=f"user has no active rental record for book ID {book_id}"
        )
    if cur_book_rentals < copies:
        raise InvalidRentalReturnException(
            book_id=book_id,
            message=f"attempting to return {copies} copies but only {cur_book_rentals} were rented."
        )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{BOOKS_URI}/return/{copies}/{book_id}"
            )
            response.raise_for_status()
        data = response.json()

    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 409:
            raise BookNotAvailableException(book_id)  # book is not available
        elif exc.response.status_code == 404:
            raise BookServiceException(f"Book not found: {book_id}")
        else:
            raise BookServiceException(f"Book service error: {exc.response.status_code}")

    except httpx.HTTPError as e:
        raise BookServiceException(f"Failed to contact book service: {str(e)}")

    try:
        result = await user_model.return_book(db, user_id, book_id, copies)
        if not result:
            UserServiceException("Failed to return book")

        return result
    except sqlite3.OperationalError as db_err:
        # Step 3: If DB update fails, revert PATCH to restore book state
        try:
            async with httpx.AsyncClient() as client:
                revert_response = await client.patch(f"{BOOKS_URI}/rent/{copies}/{book_id}")
                revert_response.raise_for_status()

        except httpx.HTTPError as revert_err:
            raise BookServiceException(
                "Critical: DB update failed AND book revert failed. "
                "System may be in inconsistent state. Logged for manual intervention."
            ) from revert_err

        raise UserServiceException(f"Failed to update user record: {str(db_err)}")
