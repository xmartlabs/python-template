from typing import AsyncIterator, Iterator

from fastapi import Depends, Request

from src.core.database import (
    AsyncSession,
    Session,
    SessionLocal,
    async_session_generator,
)
from src.core.security import AuthManager
from src.models import User


def db_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def async_db_session() -> AsyncIterator[AsyncSession]:
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


def get_user(request: Request, session: Session = Depends(db_session)) -> User:
    manager = AuthManager()
    return manager(request=request, session=session)
