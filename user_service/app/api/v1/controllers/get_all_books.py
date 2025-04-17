import sqlite3
import uuid
import httpx

from sqlalchemy.ext.asyncio import AsyncSession

from app.common.settings import settings
from app.exceptions.custom_exceptions import BookNotFoundException, BookNotAvailableException, BookServiceException, \
    UserServiceException, CredentialsException
from app.models import user_model


BOOKS_URI = settings.BOOK_SERVICE_URI

async def get_all_books():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BOOKS_URI}/all",
                headers={
                    "Service-Token": settings.API_KEY
                }
            )
            response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    except httpx.HTTPStatusError as exc:
            raise BookServiceException(f"Book service error: {exc.response.status_code}")

    except httpx.HTTPError as e:
        raise BookServiceException(f"Failed to contact book service: {str(e)}")

