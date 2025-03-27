import time
from datetime import datetime, timedelta, timezone
from typing import AsyncGenerator

from httpx import AsyncClient, Response
from jose import jwt
from mock import patch

from src.core.config import settings
from src.core.security import AuthManager, PasswordManager
from src.helpers.dates import parse_datetime
from src.models import User
from src.tests.base import BASE_URL, async_session_generator


class TestUser:
    SIGNUP_URL = f"{BASE_URL}/users"
    LOGIN_URL = f"{BASE_URL}/users/login"
    ME_URL = f"{BASE_URL}/users/me"

    TEST_EMAIL = "test@test.com"
    TEST_PASSWORD = "password"
    TEST_PAYLOAD = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    BAD_TOKEN = f"Bearer {jwt.encode({'oops': 'oops'}, 'oops')}"

    async def check_user_token(self, token: str) -> None:
        """
        Checks that a user with email TEST_EMAIL and password TEST_PASSWORD exists
        in the DB, and that the token provided belongs to that user
        """
        async_session = async_session_generator()
        async with async_session() as session:
            user = await User.objects(session).get(User.email == self.TEST_EMAIL)
            await session.refresh(user)
            assert user is not None
            assert user.email == self.TEST_EMAIL
            assert PasswordManager.verify_password(self.TEST_PASSWORD, user.password)
            true_user = await AuthManager().get_user_from_token(token, session)
            await session.refresh(true_user)
            assert user == true_user

    def check_login_fail(self, response: Response) -> None:
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid email or password"

    def check_me_response(self, response: Response) -> None:
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == self.TEST_EMAIL
        assert data["is_active"] == True  # noqa: E712
        assert data["is_superuser"] == False  # noqa: E712

    async def test_signup(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        expected_expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

        response = await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        assert response.status_code == 201
        data = response.json()
        expires_at = parse_datetime(data["expires_at"])
        assert expires_at - expected_expire < timedelta(seconds=1)
        assert data["token_type"] == "Bearer"
        token = data["access_token"]
        await self.check_user_token(token=token)

    async def test_signup_wrong_shema(self, async_client: AsyncClient) -> None:
        response = await async_client.post(self.SIGNUP_URL)
        assert response.status_code == 422

    async def test_signup_dup_emails(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        response = await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        assert response.status_code == 409
        data = response.json()
        assert data["detail"] == "Email address already in use"

    async def test_login(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        expected_expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        response = await async_client.post(self.LOGIN_URL, json=self.TEST_PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        expires_at = parse_datetime(data["expires_at"])
        assert expires_at - expected_expire < timedelta(seconds=1)
        assert data["token_type"] == "Bearer"
        token = data["access_token"]
        await self.check_user_token(token=token)

    async def test_login_wrong_shema(self, async_client: AsyncClient) -> None:
        response = await async_client.post(self.LOGIN_URL)
        assert response.status_code == 422

    async def test_login_fail(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        response = await async_client.post(self.LOGIN_URL, json=self.TEST_PAYLOAD)
        self.check_login_fail(response=response)

    async def test_login_bad_password(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        payload = {"email": self.TEST_EMAIL, "password": "oops"}
        response = await async_client.post(self.LOGIN_URL, json=payload)
        self.check_login_fail(response=response)

    async def test_me_header(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        sign_up_resp = await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        data = sign_up_resp.json()
        token = f"Bearer {data['access_token']}"
        async_client.cookies.clear()
        response = await async_client.get(
            self.ME_URL, headers={AuthManager.header_name: token}
        )
        self.check_me_response(response=response)

    async def test_me_cookie(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        response = await async_client.get(self.ME_URL)
        self.check_me_response(response=response)

    async def test_me_unauthenticated(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        response = await async_client.get(self.ME_URL)
        assert response.status_code == 401

    async def test_me_bad_access_token(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        async_client.cookies.clear()
        response = await async_client.get(
            self.ME_URL, headers={AuthManager.header_name: self.BAD_TOKEN}
        )
        assert response.status_code == 401

    async def test_me_bad_cookie(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        async_client.cookies.clear()
        async_client.cookies.set(name=AuthManager.cookie_name, value=self.BAD_TOKEN)
        response = await async_client.get(self.ME_URL)
        assert response.status_code == 401

    @patch.object(settings, "access_token_expire_minutes", 0.02)
    async def test_expired_token(
        self, reset_database: AsyncGenerator, async_client: AsyncClient
    ) -> None:
        await async_client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        time.sleep(3)
        response = await async_client.get(self.ME_URL)
        assert response.status_code == 401
