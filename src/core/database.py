import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Generic, Sequence, Type, TypeVar

from fastapi import HTTPException
from sqlalchemy import ExceptionContext, func, select
from sqlalchemy.event import listens_for
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declarative_mixin,
    declared_attr,
    mapped_column,
)
from sqlalchemy.sql import Select

from src.core.config import settings
from src.helpers.casing import snakecase
from src.helpers.sql import random_uuid, utcnow

# Async engine and session
engine: AsyncEngine = create_async_engine(
    url=str(settings.async_database_url),
    pool_pre_ping=settings.database_pool_pre_ping,
    pool_size=settings.database_pool_size,
    pool_recycle=settings.database_pool_recycle,
    max_overflow=settings.database_max_overflow,
)


@listens_for(engine.sync_engine, "handle_error")
def _on_handle_error(context: ExceptionContext) -> None:
    """
    Handles errors that occur during SQL operations and logs them.
    This function is triggered when an error event occurs for the PostgreSQL engine.
    It logs the error and sets the `is_disconnect` attribute to True if the error
    is related to a connection issue, prompting SQLAlchemy to retry the connection.

    Args:
        context (ExceptionContext): The context of the exception, containing details about the SQLAlchemy exception.

    Returns:
        None: this returns nothing.
    """
    logging.warning(
        f"handle_error event triggered for PostgreSQL engine: {context.sqlalchemy_exception}"
    )
    if "Can't connect to PostgreSQL server on" in str(context.sqlalchemy_exception):
        # Setting is_disconnect to True should tell SQLAlchemy treat this as a connection error and retry
        context.is_disconnect = True  # type: ignore

    return None


def async_session_generator() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
    )


class SQLBase(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)

    @classmethod
    def objects(cls: Type["_Model"], session: AsyncSession) -> "Objects[_Model]":
        return Objects(cls, session)


_Model = TypeVar("_Model", bound=SQLBase)


class Objects(Generic[_Model]):
    cls: Type[_Model]
    session: AsyncSession
    base_statement: Select
    queryset_filters: Any = None

    def __init__(
        self,
        cls: Type[_Model],
        session: AsyncSession,
        *queryset_filters: Any,
    ) -> None:
        self.cls = cls
        self.session = session
        base_statement = select(cls)
        if queryset_filters:
            self.queryset_filters = queryset_filters
            base_statement = base_statement.where(*queryset_filters)
        self.base_statement = base_statement

    async def all(self) -> Sequence[_Model]:
        result = await self.session.execute(self.base_statement)
        return result.scalars().unique().all()

    async def get(self, *where_clause: Any) -> _Model | None:
        statement = self.base_statement.where(*where_clause)
        result = await self.session.execute(statement)
        return result.unique().scalar_one_or_none()

    async def get_or_404(self, *where_clause: Any) -> _Model:
        obj = await self.get(*where_clause)
        if obj is None:
            raise HTTPException(
                status_code=404, detail=f"{self.cls.__name__} not found"
            )
        return obj

    async def get_all(self, *where_clause: Any) -> Sequence[_Model]:
        statement = self.base_statement.where(*where_clause)
        result = await self.session.execute(statement)
        return result.scalars().unique().all()

    async def count(self, *where_clause: Any) -> int:
        statement = select(func.count()).select_from(self.cls)
        if self.queryset_filters:
            statement = statement.where(*self.queryset_filters)
        if where_clause:
            statement = statement.where(*where_clause)

        result = await self.session.execute(statement)
        return result.scalar_one()

    async def create(self, data: Dict[str, Any]) -> _Model:
        obj = self.cls(**data)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def bulk_create(self, data: Sequence[Dict[str, Any]]) -> Sequence[_Model]:
        objs = [self.cls(**item) for item in data]
        self.session.add_all(objs)
        await self.session.commit()
        return objs


@declarative_mixin
class TableIdMixin:
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, server_default=random_uuid()
    )


@declarative_mixin
class DatedTableMixin(TableIdMixin):
    created_at: Mapped[datetime] = mapped_column(server_default=utcnow())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=utcnow(), onupdate=datetime.now(timezone.utc)
    )
