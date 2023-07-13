from typing import Iterator

from fastapi import Cookie, Depends, HTTPException

from src.core.database import Session, SessionLocal
from src.core.security import AuthManager
from src.models import User


def db_session() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
