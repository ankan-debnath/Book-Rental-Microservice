import uuid
import sqlite3
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped

from app.auth.password import get_password_hash
from app.exceptions.custom_exceptions import UserAlreadyExistsException, UserServiceException
from app.models.user_model import if_user_exists
from app.schemas.user import CreateUserRequest
from app.models import user_model, UserModel, RentalModel


async def get_rental_details(
        db: AsyncSession,
        user_id: uuid.UUID
) ->  Mapped[list[RentalModel]]:

    try:
        result = await user_model.get_rental_details(db, user_id)



        return result
    except sqlite3.OperationalError as db_err:

        raise UserServiceException(f"Failed to update user record: {str(db_err)}")

