from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Token(BaseModel):
    token_type: str = "Bearer"
    access_token: str
    expires_at: datetime


class TokenPayload(BaseModel):
    user_id: UUID
