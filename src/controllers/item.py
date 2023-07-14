from uuid import UUID

from src import models
from src.api.v1 import schemas
from src.core.database import Session


class ItemController:
    @staticmethod
    def create(
        item_data: schemas.ItemCreate, owner_id: UUID, session: Session
    ) -> models.Item:
        item_data = schemas.Item(owner_id=owner_id, **item_data.dict())
        item = models.Item.objects(session).create(item_data.dict())
        return item
