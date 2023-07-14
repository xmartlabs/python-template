from uuid import UUID

from src.api.v1.schemas import ItemCreate
from src.core.database import Session
from src.models import Item


class ItemController:
    @staticmethod
    def create(item_data: ItemCreate, owner_id: UUID, session: Session) -> Item:
        item = Item.objects(session).create(
            Item.name == item_data.name,
            Item.description == item_data.description,
            Item.is_public == item_data.is_public,
            Item.owner_id == owner_id,
        )
        return item
