from typing import Any, Callable, Iterator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.api.dependencies import db_session
from src.core.config import settings
from src.core.database import SQLBase
from src.main import app

BASE_URL = "/api/v1"

database_url = settings.test_database_url
assert database_url is not None, "TEST_DATABASE_URL must be defined"

engine = create_engine(database_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db() -> Iterator[Session]:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[db_session] = override_get_db

client = TestClient(app)


def reset_database(test: Callable) -> Callable:
    """
    Decorator that creates all the tables before the test,
    and drops all of them after running it.
    """

    def decorator(*args: Any, **kwargs: Any) -> Any:
        try:
            SQLBase.metadata.create_all(bind=engine)
            result = test(*args, **kwargs)
        finally:
            SQLBase.metadata.drop_all(bind=engine)
        return result

    return decorator
