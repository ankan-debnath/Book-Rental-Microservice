import uuid
import sqlite3
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
import httpx

from app.auth.password import get_password_hash
from app.common.settings import settings
from app.exceptions.custom_exceptions import UserAlreadyExistsException, UserServiceException, BookServiceException
from app.models.user_model import if_user_exists
from app.schemas.user import CreateUserRequest
from app.models import user_model, UserModel, RentalModel


async def get_rental_details(
        db: AsyncSession,
        user_id: uuid.UUID
) ->  Mapped[list[RentalModel]] | None:

    try:
        rentals = await user_model.get_rental_details(db, user_id)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{settings.BOOK_SERVICE_URI}/list",
                    headers={
                        "Service-Token": settings.API_KEY
                    },
                    json={
                        "book_ids" : [str(rental.book_id) for rental in rentals]
                    }
                )
                response.raise_for_status()
            data = response.json().get("data", [])
        except httpx.HTTPStatusError as exc:
            raise BookServiceException(f"Book service error: {exc.response.status_code}")

        return [ {rental.id : data[rental.book_id]} for rental in rentals ]

    except sqlite3.OperationalError as db_err:

        raise UserServiceException(f"Failed to update user record: {str(db_err)}")

