import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.custom_exceptions import NoDataToUpdateException, UserAlreadyExistsException
from app.models import UserModel
from app.schemas.user import UpdateUserRequest, UpdateUserPatchRequest
from app.models import user_model


async def update_user_patch(session: AsyncSession, user_id: uuid.UUID, user: UpdateUserPatchRequest) -> UserModel:
    user: dict = user.model_dump(exclude_unset=True)
    if not user:
        raise NoDataToUpdateException()

    try:
        updated_user = await user_model.update_user(session, user_id, user)
    except IntegrityError:
        raise UserAlreadyExistsException(**user)

    return updated_user