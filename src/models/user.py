import typing
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import Select

from src.core.database import DatedTableMixin, Objects, Session, SQLBase

if typing.TYPE_CHECKING:
    from src.models import Item


class User(SQLBase, DatedTableMixin):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    items: Mapped[List["Item"]] = relationship("Item", back_populates="owner")

    def __str__(self) -> str:
        return self.email

    @classmethod
    def actives(cls, session: Session) -> Objects["User"]:
        return Objects(cls, session, User.is_active == True)  # noqa: E712

    def get_items(self) -> Select:
        from src.models import Item

        statement = select(Item).filter(Item.owner_id == self.id)
        return statement

    def get_public_items(self) -> Select:
        from src.models import Item

        statement = self.get_items().filter(Item.is_public == True)  # noqa: E712
        return statement
