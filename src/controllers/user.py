from fastapi import HTTPException

from src.api.v1.schemas import UserCreate
from src.core.database import AsyncSession
from src.core.security import PasswordManager
from src.models import User


class UserController:
    @staticmethod
    async def create(user_data: UserCreate, session: AsyncSession) -> User:
        user = await User.objects(session).get(User.email == user_data.email)
        if user:
            raise HTTPException(status_code=409, detail="Email address already in use")
        hashed_password = PasswordManager.get_password_hash(user_data.password)
        user_data.password = hashed_password
        user = await User.objects(session).create(user_data.model_dump())
        await session.refresh(user)
        return user

    @staticmethod
    async def login(user_data: UserCreate, session: AsyncSession) -> User:
        login_exception = HTTPException(
            status_code=401, detail="Invalid email or password"
        )
        user = await User.objects(session).get(User.email == user_data.email)
        if not user:
            raise login_exception
        if not PasswordManager.verify_password(user_data.password, user.password):
            raise login_exception
        await session.refresh(user)
        return user
