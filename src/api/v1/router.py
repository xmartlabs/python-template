from fastapi import APIRouter

from src.api.v1.routers import item, task, user

v1_router = APIRouter()
v1_router.include_router(user.router, prefix="/users")
v1_router.include_router(item.router, prefix="/items")
v1_router.include_router(
    task.router, tags=["Distributed Tasks Queue - Celery"], prefix="/tasks"
)
