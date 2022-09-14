from typing import List

from app.core.models import UUIDModel
from app.db.repositories.base import BaseRepository
from app.user.models import UserCreate, UserRead, UserInDB

GET_USERS_QUERY = """
    SELECT uuid, nickname, role, created_at, updated_at
    FROM users;
"""

CREATE_USER_QUERY = """
    INSERT INTO users (nickname, role)
    VALUES (:nickname, :role)
    RETURNING uuid, nickname, role;
"""


class UsersRepository(BaseRepository):
    """"
    All database actions associated with the User resource
    """

    async def create_user(self, *, new_user: UserCreate) -> UserInDB:
        query_values = new_user.dict()
        user = await self.db.fetch_one(query=CREATE_USER_QUERY, values=query_values)

        return UserInDB(**user)

    async def get_users(self) -> List[UserRead]:
        user_records = await self.db.fetch_all(query=GET_USERS_QUERY)

        return [UserRead(**u) for u in user_records]

