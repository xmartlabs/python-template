from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str = "bearer"
    access_token: str
    expires_in: int


class TokenPayload(BaseModel):
    user_id: UUID
