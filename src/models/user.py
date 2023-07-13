from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import DatedTableMixin, Objects, Session, SQLBase


class User(SQLBase, DatedTableMixin):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    @classmethod
    def actives(cls, session: Session) -> Objects["User"]:
        return Objects(cls, session, User.is_active == True)  # noqa: E712
