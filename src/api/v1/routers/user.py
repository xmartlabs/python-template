from typing import Any

from fastapi import APIRouter, Depends, Response

from src import models
from src.api.dependencies import db_session, get_user
from src.api.v1 import schemas
from src.controllers import UserController
from src.core.database import Session
from src.core.security import AuthManager

router = APIRouter()


@router.post("", response_model=schemas.Token, status_code=201)
def create(
    response: Response, user_data: schemas.UserCreate, use_cookie: bool = False, session: Session = Depends(db_session)
) -> schemas.Token:
    user = UserController.create(user_data=user_data, session=session)
    return AuthManager.create_access_token(user)


@router.post("/login", response_model=schemas.Token)
def login(
    response: Response, user_data: schemas.UserCreate, use_cookie: bool = False,  session: Session = Depends(db_session)
) -> schemas.Token:
    pass


@router.get("/me", response_model=schemas.User)
def get_user_info(user: models.User = Depends(AuthManager)) -> Any:
    return user
