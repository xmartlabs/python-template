from datetime import datetime, timedelta
from typing import Tuple

from fastapi import HTTPException, Request, Response
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError

from src.api.v1.schemas import Token, TokenPayload
from src.core.config import settings
from src.core.database import Session
from src.models import User


class PasswordManager:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return cls.pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return cls.pwd_context.hash(password)


class AuthManager:
    algorithm = "HS256"
    cookie_name = "access-token"
    header_name = "Authorization"
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    accept_cookie = settings.accept_cookie
    accept_header = settings.accept_token

    @classmethod
    def create_access_token(
        cls, user: User, expires_delta: timedelta | None = None
    ) -> Tuple[str, datetime]:
        expires = datetime.utcnow() + (
            expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
        )
        claims = {"exp": expires, "user_id": str(user.id)}
        token = jwt.encode(
            claims=claims, key=settings.jwt_signing_key, algorithm=cls.algorithm
        )
        return token, expires

    @classmethod
    def _set_cookie(cls, response: Response, token: str) -> None:
        response.set_cookie(key=cls.cookie_name, value=token, httponly=True)

    @classmethod
    def process_login(cls, user: User, response: Response) -> Token | None:
        token, expires = cls.create_access_token(user)
        if cls.accept_cookie:
            cls._set_cookie(response=response, token=token)
        if cls.accept_header:
            return Token(access_token=token, expires_at=expires)
        return None

    def get_user_from_token(self, token: str, session: Session) -> User:
        try:
            payload = jwt.decode(
                token=token, key=settings.jwt_signing_key, algorithms=self.algorithm
            )
            token_data = TokenPayload(**payload)
        except (JWTError, ValidationError):
            raise self.credentials_exception
        user = User.objects(session).get(User.id == token_data.user_id)
        if not user:
            raise self.credentials_exception
        return user

    def _get_token_from_cookie(self, request: Request) -> str | None:
        token = request.cookies.get(self.cookie_name)
        return token

    def _get_token_from_header(self, request: Request) -> str | None:
        authorization = request.headers.get(self.header_name)
        scheme, token = get_authorization_scheme_param(authorization)
        if scheme.lower() != "bearer":
            return None
        return token

    def _get_token(self, request: Request) -> str:
        token = None
        if self.accept_header:
            token = self._get_token_from_header(request)
        if not token and self.accept_cookie:
            token = self._get_token_from_cookie(request)
        if not token:
            raise self.credentials_exception
        return token

    def __call__(self, request: Request, session: Session) -> User:
        token = self._get_token(request)
        return self.get_user_from_token(token, session)
