import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import UserNotFoundException
from app.models import user_model


async def get_user(session: AsyncSession, user_id: uuid.UUID):
    cur_user = await user_model.get_user(session, user_id)
    if not cur_user:
        raise UserNotFoundException(user_id=user_id)

    return cur_user