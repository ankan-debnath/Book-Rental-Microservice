import sqlite3
import uuid
import httpx

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import BookNotFoundException, BookNotAvailableException, BookServiceException, \
    UserServiceException
from app.models import user_model


BOOKS_URI = "http://127.0.0.1:8000/v1/books"

async def rent_book(db: AsyncSession, user_id: uuid.UUID, book_id: uuid.UUID, copies:int):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{BOOKS_URI}/rent/{copies}/{book_id}"
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
        result = await user_model.rent_book(db, user_id, book_id)
        if not result:
            UserServiceException("Failed to rent book")

        return result
    except sqlite3.OperationalError as db_err:
        # Step 3: If DB update fails, revert PATCH to restore book state
        try:
            async with httpx.AsyncClient() as client:
                revert_response = await client.patch(f"{BOOKS_URI}/return/{copies}/{book_id}")
                revert_response.raise_for_status()

        except httpx.HTTPError as revert_err:
            # Inconsistent state – both book and user services failed!
            # log_critical_failure(
            #     book_id=book_id,
            #     user_id=user_id,
            #     message="User DB update failed and book revert failed.",
            #     errors={
            #         "db_error": str(db_err),
            #         "revert_error": str(revert_err),
            #     }
            # )
            raise BookServiceException(
                "Critical: DB update failed AND book revert failed. "
                "System may be in inconsistent state. Logged for manual intervention."
            ) from revert_err

        raise UserServiceException(f"Failed to update user record: {str(db_err)}")

