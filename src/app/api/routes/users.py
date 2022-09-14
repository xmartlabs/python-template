from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from app.api.dependencies.database import get_repository
from app.core.models import UUIDModel
from app.db.repositories.users import UsersRepository
from app.user.models import UserCreate, UserBase, UserPublic

router = APIRouter()


@router.get("/users", response_model=List[UserBase], name="users:get-users")
async def get_users(
        user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> List[UserBase]:
    return await user_repo.get_users()


@router.post("/users", response_model=UserPublic, name="users:create-user", status_code=HTTP_201_CREATED)
async def create_new_user(
        new_user: UserCreate = Body(..., embed=True),
        user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UserPublic:
    created_user = await user_repo.create_user(new_user=new_user)

    return created_user
