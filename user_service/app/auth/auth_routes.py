from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.password import verify_password, create_access_token
from app.common.db import get_session
from app.models import user_model
from app.schemas.user import Response, Token

router = APIRouter(prefix="/token")

@router.post("")
async def create_token(
    db : AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm)
) -> Token :

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={"success" : False, "message": "Could not validate credentials"},
        headers={"WWW-Authenticate": "Bearer"}
    )

    user = await user_model.if_user_email_exists(db, form_data.username)

    if not user:
        raise credentials_exception

    if verify_password(form_data.password, user.password):
        access_token = create_access_token(({ "user_id" : user.user_id }))
        return Token(access_token=access_token, grant_type="bearer")
    else:
        raise credentials_exception