from fastapi import APIRouter

from app.api.v1.routes.user_routes import router as r1

router = APIRouter(prefix="/v1")

router.include_router(r1)
