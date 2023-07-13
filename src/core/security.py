from datetime import datetime, timedelta

from fastapi import HTTPException, Response, Request
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
    accept_header = settings.accept_header


    def create_access_token(self, user: User, expires_delta: timedelta | None = None) -> Token:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes
            )
        claims = {"exp": expire, "user_id": str(user.id)}
        token = jwt.encode(claims=claims, key=settings.jwt_signing_key, algorithm=self.algorithm)
        return Token(access_token=token, expires_in=expire)


    def _get_user_from_token(self, token: str, session: Session) -> User:
        try:
            payload = jwt.decode(
                token=token, key=settings.jwt_signing_key, algorithms=self.algorithm
            )
            token_data = TokenPayload(**payload)
        except (JWTError, ValidationError):
            raise self.credentials_exception
        user = User.objects(session).get_or_exception(
            User.id == token_data.user_id, self.credentials_exception
        )
        return user
    
    def _set_cookie(self, response: Response, token: str) -> None:
        response.set_cookie(key=self.cookie_name, value=token, httponly=True)

    
    def _get_token_from_cookie(self, request: Request) -> str | None:
        token = request.cookies.get(self.cookie_name)
        # To prevent returning ""
        return token if token else None
    

    def _get_token_from_header(self, request: Request) -> str | None:
        token = request.headers.get(self.header_name)
        # To prevent returning ""
        return token if token else None
    

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
        return self._get_user_from_token(token, session)

