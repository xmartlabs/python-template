from pydantic import BaseModel


class ItemCreate(BaseModel):
    name: str
    description: str | None
    is_public: bool = True


class Item(ItemCreate):
    class Config:
        orm_mode = True
