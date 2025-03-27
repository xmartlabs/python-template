from typing import Any

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependencies import db_session, get_user
from src.api.v1.schemas import BulkItemCreate, Item, ItemCreate
from src.controllers import ItemController
from src.core.database import AsyncSession
from src.models import User

router = APIRouter()


@router.get("", response_model=Page[Item])
async def get_items(
    user: User = Depends(get_user), session: AsyncSession = Depends(db_session)
) -> Any:
    return await paginate(session, user.get_items())


@router.post("", response_model=Item, status_code=201)
async def create_item(
    item_data: ItemCreate,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(db_session),
) -> Any:
    return await ItemController.create(
        item_data=item_data, owner_id=user.id, session=session
    )


@router.get("/async", response_model=Page[Item])
async def get_items_async(
    user: User = Depends(get_user),
    session: AsyncSession = Depends(db_session),
) -> Any:
    """Get items asynchronously."""
    return await paginate(session, user.get_items())


@router.post("/async", response_model=list[Item], status_code=201)
async def create_item_async(
    item_data: BulkItemCreate,
    user: User = Depends(get_user),
    session: AsyncSession = Depends(db_session),
) -> Any:
    """Create items asynchronously."""
    return await ItemController.bulk_create(
        items_data=item_data.items, owner_id=user.id, async_session=session
    )
