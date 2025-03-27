import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import ASGITransport, AsyncClient

from src.core.database import SQLBase
from src.tests.base import app, async_engine


@pytest.fixture(scope="function")
async def reset_database() -> AsyncGenerator:
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLBase.metadata.drop_all)
        await conn.run_sync(SQLBase.metadata.create_all)

    yield  # Aquí se ejecuta el test

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLBase.metadata.drop_all)


@pytest.fixture
async def async_client() -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Forzar pytest-asyncio a usar un solo loop por sesión"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
