from typing import Iterator

from fastapi import Depends, Request

from src.core.database import Session, SessionLocal
from src.core.security import AuthManager
from src.models import User


def db_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user(request: Request, session: Session = Depends(db_session)) -> User:
    manager = AuthManager()
    return manager(request=request, session=session)
