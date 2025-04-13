from starlette import status
from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/token")

@router.post("")
async def create_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.username)
    if form_data.username == "ankan":
        return {"access_token" : "token", "grant_type" : "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)