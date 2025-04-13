from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

bearer = OAuth2PasswordBearer(tokenUrl="/token")


SECRET_KEY: str = "super-secret-key"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


async def get_current_user(token: str = Depends(bearer)):
    return {"user" : 1}