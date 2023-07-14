from typing import Any

from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src.api.dependencies import db_session, get_user
from src.api.v1.schemas import Item, ItemCreate
from src.controllers import ItemController
from src.core.database import Session
from src.models import User

router = APIRouter()


@router.get("", response_model=Page[Item])
def get_items(
    user: User = Depends(get_user), session: Session = Depends(db_session)
) -> Any:
    return paginate(session, user.get_items())


@router.post("", response_model=Item, status_code=201)
def create_item(
    item_data: ItemCreate,
    user: User = Depends(get_user),
    session: Session = Depends(db_session),
) -> Any:
    return ItemController.create(item_data=item_data, owner_id=user.id, session=session)
