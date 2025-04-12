from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import UserAlreadyExistsException
from app.models.user_model import if_user_exists
from app.schemas.user import CreateUserRequest
from app.models import user_model, UserModel


async def add_user(
        session: AsyncSession,
        user: CreateUserRequest
) -> UserModel:
    existing = await if_user_exists(session, user)
    if existing:
        raise UserAlreadyExistsException(email=user.email)

    try:
        data = await user_model.create_user(session, user)
    except IntegrityError:
        raise UserAlreadyExistsException(email=user.email)

    return data


