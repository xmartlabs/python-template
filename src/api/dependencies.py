from typing import AsyncIterator

from fastapi import Depends, Request

from src.core.database import AsyncSession, async_session_generator
from src.core.security import AuthManager
from src.models import User


async def db_session() -> AsyncIterator[AsyncSession]:
    session = None
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
    except Exception:
        if session is not None:
            await session.rollback()
        raise
    finally:
        if session is not None:
            await session.close()


async def get_user(request: Request, session: AsyncSession = Depends(db_session)) -> User:
    manager = AuthManager()
    return await manager(request=request, session=session)
