import uuid

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.password import get_password_hash
from app.exceptions.custom_exceptions import (
    NoDataToUpdateException,
    UserAlreadyExistsException,
    UserNotFoundException
)
from app.models import UserModel
from app.schemas.user import UpdateUserRequest, UpdateUserPatchRequest
from app.models import user_model


async def update_user_patch(session: AsyncSession, user_id: uuid.UUID, update_details: UpdateUserPatchRequest) -> UserModel:
    update_details: dict = update_details.model_dump(exclude_unset=True)

    if "password" in update_details:
        update_details["password"] = get_password_hash(update_details["password"])


    if not update_details:
        raise NoDataToUpdateException()

    try:
        updated_user = await user_model.update_user(session, user_id, update_details)
        if not updated_user:
            raise UserNotFoundException(user_id)

    except IntegrityError:
        raise UserAlreadyExistsException(**update_details)

    return updated_user