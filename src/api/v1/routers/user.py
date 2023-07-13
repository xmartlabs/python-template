from typing import Any

from fastapi import APIRouter, Depends, Response

from src import models
from src.api.dependencies import db_session, get_user
from src.api.v1 import schemas
from src.controllers import UserController
from src.core.database import Session
from src.core.security import AuthManager

router = APIRouter()


@router.post("", status_code=201)
def create(
    response: Response,
    user_data: schemas.UserCreate,
    session: Session = Depends(db_session),
) -> schemas.Token | None:
    user = UserController.create(user_data=user_data, session=session)
    return AuthManager.process_login(user=user, response=response)


@router.post("/login")
def login(
    response: Response,
    user_data: schemas.UserCreate,
    session: Session = Depends(db_session),
) -> schemas.Token | None:
    user = UserController.login(user_data=user_data, session=session)
    return AuthManager.process_login(user=user, response=response)


@router.get("/me", response_model=schemas.User)
def get_user_info(user: models.User = Depends(get_user)) -> Any:
    return user
