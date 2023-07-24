import typing
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import DatedTableMixin, SQLBase

if typing.TYPE_CHECKING:
    from src.models import User


class Item(SQLBase, DatedTableMixin):
    name: Mapped[str]
    description: Mapped[str | None]
    is_public: Mapped[bool]
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship("User", back_populates="items")

    def __str__(self) -> str:
        return f"Item {str(self.id)[:12]}..."
