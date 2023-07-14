import typing
from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import DatedTableMixin, SQLBase

if typing.TYPE_CHECKING:
    from src.models import User


class Item(SQLBase, DatedTableMixin):
    name: Mapped[str] = mapped_column()
    description: Mapped[str | None] = mapped_column()
    is_public: Mapped[bool] = mapped_column(default=True)
    owner_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship("User", back_populates="items")
