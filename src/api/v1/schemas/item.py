from uuid import UUID

from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str | None
    is_public: bool = True


class Item(ItemCreate):
    owner_id: UUID

    class Config:
        orm_mode = True
