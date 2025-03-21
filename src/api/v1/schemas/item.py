from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    is_public: bool = True


class Item(ItemCreate):
    owner_id: UUID
    model_config = ConfigDict(from_attributes=True)


class BulkItemCreate(BaseModel):
    items: list[ItemCreate]
