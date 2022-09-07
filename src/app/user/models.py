from typing import Optional

from sqlalchemy import Column, event
from sqlalchemy.databases import postgres
from sqlmodel import Field, SQLModel

from app.core.models import TimestampModel, UUIDModel

tablename = "users"

hrs_role_type = postgres.ENUM(
    "mage",
    "assassin",
    "warrior",
    "priest",
    "tank",
    name=f"{tablename}_role"
)


@event.listens_for(SQLModel.metadata, "before_create")
def _create_enums(metadata, conn, **kw):  # noqa: indirect usage
    hrs_role_type.create(conn, checkfirst=True)


class UserBase(SQLModel):
    nickname: str = Field(max_length=255, nullable=False)
    role: Optional[str] = Field(
        sa_column=Column(
            "role",
            hrs_role_type,
            nullable=True
        )
    )


class User(
    TimestampModel,
    UserBase,
    UUIDModel,
    table=True
):
    __tablename__ = f"{tablename}"


class UserRead(UserBase, UUIDModel):
    ...


class UserCreate(UserBase):
    ...


class UserPatch(UserBase):
    nickname: Optional[str] = Field(max_length=255)
