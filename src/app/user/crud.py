from select import select
from uuid import UUID

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy import delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.user.models import UserCreate, User, UserPatch


class UsersCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: UserCreate) -> User:
        values = data.dict()

        user = User(**values)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def get(self, user_id: str | UUID) -> User:
        statement = select(
            User
        ).where(
            User.uuid == user_id
        )
        result = await self.session.execute(statement=statement)
        user = result.scalar_one_or_none()  # type: User | None

        if user is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="The user hasn't been found!"
            )

        return user

    async def patch(self, user_id: str | UUID, data: UserPatch) -> User:
        user = await self.get(user_id=user_id)
        values = data.dict(exclude_unset=True)

        for k, v in values.items():
            setattr(user, k, v)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete(self, user_id: str | UUID) -> bool:
        statement = delete(
            User
        ).where(
            User.uuid == user_id
        )

        await self.session.execute(statement=statement)
        await self.session.commit()

        return True
