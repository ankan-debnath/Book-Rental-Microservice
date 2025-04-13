from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED

from app.common.db import get_session
from app.schemas.user import CreateUserRequest, Response, UserSchema
from app.api.v1 import controllers

router = APIRouter(prefix="/user")


@router.post("", status_code=HTTP_201_CREATED)
async def create_user(
        user: CreateUserRequest,
        session:AsyncSession =  Depends(get_session)
) -> Response:

    new_user = await controllers.add_user(session, user)
    return Response(
        success=True,
        message="User created successfully",
        data=UserSchema.model_validate(new_user)
    )
