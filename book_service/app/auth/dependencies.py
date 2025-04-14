from fastapi import Header, HTTPException

from app.common.settings import settings


async def verify_token(service_token: str = Header(...)) -> bool:
    print(service_token)
    if service_token != settings.SERVICE_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized service")
    return True