import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import UserNotFoundException
from app.models import UserModel
from app.models import user_model


async def delete_user(session: AsyncSession, user_id: uuid.UUID) -> UserModel:
    deleted_user = await user_model.delete_user(session, user_id)

    if not deleted_user:
        raise UserNotFoundException(user_id)

    return deleted_user