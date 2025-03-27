from typing import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.api.dependencies import db_session
from src.core.config import settings
from src.main import app

BASE_URL = "/api/v1"

database_url = str(settings.async_database_url)
assert database_url is not None, "DATABASE_URL must be defined"

async_engine = create_async_engine(
    database_url,
    pool_pre_ping=settings.database_pool_pre_ping,
    pool_size=settings.database_pool_size,
    pool_recycle=settings.database_pool_recycle,
    max_overflow=settings.database_max_overflow,
)


def async_session_generator() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )


async def override_get_db() -> AsyncIterator[AsyncSession]:
    try:
        async_session = async_session_generator()
        async with async_session() as session:
            yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()


app.dependency_overrides[db_session] = override_get_db
