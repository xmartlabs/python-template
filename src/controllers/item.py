from typing import Sequence
from uuid import UUID

from src import models
from src.api.v1 import schemas
from src.core.database import AsyncSession


class ItemController:
    @staticmethod
    async def create(
        item_data: schemas.ItemCreate, owner_id: UUID, session: AsyncSession
    ) -> models.Item:
        item_data = schemas.Item(owner_id=owner_id, **item_data.model_dump())
        item = await models.Item.objects(session).create(item_data.model_dump())
        await session.refresh(item)
        return item

    @staticmethod
    async def bulk_create(
        items_data: Sequence[schemas.ItemCreate],
        owner_id: UUID,
        async_session: AsyncSession,
    ) -> Sequence[models.Item]:
        items_data = [
            schemas.Item(owner_id=owner_id, **item_data.model_dump())
            for item_data in items_data
        ]
        items = await models.Item.objects(async_session).bulk_create(
            [item_data.model_dump() for item_data in items_data]
        )
        for item in items:
            await async_session.refresh(item)

        return items
