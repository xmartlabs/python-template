from fastapi import APIRouter

from app.api.routes.ping import router as ping_router
from app.api.routes.users import router as users_router


router = APIRouter()


router.include_router(ping_router)
router.include_router(users_router)
