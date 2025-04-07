from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, Response
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from src import models
from src.api.dependencies import db_session, get_user
from src.api.v1 import schemas
from src.api.v1.schemas import Item, Token, UserCreate
from src.controllers import UserController
from src.core.database import Session
from src.core.security import AuthManager
from src.core.trace import tracer_provider

router = APIRouter()


@router.post("", status_code=201)
def signup(
    response: Response,
    user_data: UserCreate,
    session: Session = Depends(db_session),
) -> Token | None:
    user = UserController.create(user_data=user_data, session=session)
    return AuthManager.process_login(user=user, response=response)


@router.post("/login")
def login(
    response: Response,
    user_data: UserCreate,
    session: Session = Depends(db_session),
) -> Token | None:
    user = UserController.login(user_data=user_data, session=session)
    return AuthManager.process_login(user=user, response=response)


@router.get("/me", response_model=schemas.User)
def me(user: models.User = Depends(get_user)) -> Any:
    return user


@router.get("/{user_id}/items", response_model=Page[Item])
def get_public_items(user_id: UUID, session: Session = Depends(db_session)) -> Any:
    # We can't use the @instrument decorator here because it will collide with the
    # FastAPIinstrumentor and cause the span to be created twice.
    # So we need to create the span manually.
    with tracer_provider.get_tracer(__name__).start_as_current_span("get_public_items"):
        user = models.User.objects(session).get_or_404(models.User.id == user_id)
    return paginate(session, user.get_public_items())
