from fastapi import APIRouter
from fastapi.params import Depends

from app.api.v1.routes.register_route import router as r1
from app.api.v1.routes.user_routes import router as r2
from app.auth.auth import get_current_user

router = APIRouter(prefix="/v1")

router.include_router(r1)
router.include_router(r2, dependencies=[Depends(get_current_user)])
