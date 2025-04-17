import sqlite3

import jwt
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.auth.password import verify_access_token
from app.common.db import get_session
from app.exceptions.custom_exceptions import UserServiceException
from app.schemas.user import TokenData
from app.models import user_model

bearer = OAuth2PasswordBearer(tokenUrl="/token")

async def get_current_user(
        token: str = Depends(bearer),
        db: AsyncSession = Depends(get_session)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    if not token:
        raise credentials_exception

    try:
        payload = verify_access_token(token)

        user_id = payload.get("user_id", None)
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    try:
        user = await user_model.if_user_id_exists(db, user_id)

        if user is None:
            raise credentials_exception
        return user
    except sqlite3.OperationalError:
        raise UserServiceException("Failed to authenticate")