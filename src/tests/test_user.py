import time
from datetime import datetime, timedelta

from httpx import Response
from jose import jwt
from pydantic.datetime_parse import parse_datetime

from src.core.config import settings
from src.core.security import AuthManager, PasswordManager
from src.models import User
from src.tests.base import BASE_URL, TestingSessionLocal, client, reset_database


class TestUser:
    SIGNUP_URL = f"{BASE_URL}/users"
    LOGIN_URL = f"{BASE_URL}/users/login"
    ME_URL = f"{BASE_URL}/users/me"

    TEST_EMAIL = "test@test.com"
    TEST_PASSWORD = "password"
    TEST_PAYLOAD = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    BAD_TOKEN = f"Bearer {jwt.encode({'oops': 'oops'}, 'oops')}"

    def check_user_token(self, token: str) -> None:
        """
        Checks that a user with email TEST_EMAIL and password TEST_PASSWORD exists
        in the DB, and that the token provided belongs to that user
        """
        with TestingSessionLocal() as session:
            user = User.objects(session).get(User.email == self.TEST_EMAIL)
            assert user is not None
            assert user.email == self.TEST_EMAIL
            assert PasswordManager.verify_password(self.TEST_PASSWORD, user.password)
            assert user == AuthManager().get_user_from_token(token, session)

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

    @reset_database
    def test_signup(self) -> None:
        expected_expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        response = client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        assert response.status_code == 201
        data = response.json()
        expires_at = parse_datetime(data["expires_at"])
        assert expires_at - expected_expire < timedelta(seconds=1)
        assert data["token_type"] == "Bearer"
        token = data["access_token"]
        self.check_user_token(token=token)

    def test_signup_wrong_shema(self) -> None:
        response = client.post(self.SIGNUP_URL)
        assert response.status_code == 422

    @reset_database
    def test_signup_dup_emails(self) -> None:
        client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        response = client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        assert response.status_code == 409
        data = response.json()
        assert data["detail"] == "Email address already in use"

    @reset_database
    def test_login(self) -> None:
        client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        expected_expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        response = client.post(self.LOGIN_URL, json=self.TEST_PAYLOAD)
        assert response.status_code == 200
        data = response.json()
        expires_at = parse_datetime(data["expires_at"])
        assert expires_at - expected_expire < timedelta(seconds=1)
        assert data["token_type"] == "Bearer"
        token = data["access_token"]
        self.check_user_token(token=token)

    def test_login_wrong_shema(self) -> None:
        response = client.post(self.LOGIN_URL)
        assert response.status_code == 422

    @reset_database
    def test_login_fail(self) -> None:
        response = client.post(self.LOGIN_URL, json=self.TEST_PAYLOAD)
        self.check_login_fail(response=response)

    @reset_database
    def test_login_bad_password(self) -> None:
        client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        payload = {"email": self.TEST_EMAIL, "password": "oops"}
        response = client.post(self.LOGIN_URL, json=payload)
        self.check_login_fail(response=response)

    @reset_database
    def test_me_header(self) -> None:
        sign_up_resp = client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        data = sign_up_resp.json()
        token = f"Bearer {data['access_token']}"
        client.cookies.clear()
        response = client.get(self.ME_URL, headers={AuthManager.header_name: token})
        self.check_me_response(response=response)

    @reset_database
    def test_me_cookie(self) -> None:
        client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        response = client.get(self.ME_URL)
        self.check_me_response(response=response)

    @reset_database
    def test_me_unauthenticated(self) -> None:
        response = client.get(self.ME_URL)
        assert response.status_code == 401

    @reset_database
    def test_me_bad_access_token(self) -> None:
        client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        client.cookies.clear()
        response = client.get(
            self.ME_URL, headers={AuthManager.header_name: self.BAD_TOKEN}
        )
        assert response.status_code == 401

    @reset_database
    def test_me_bad_cookie(self) -> None:
        client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        client.cookies.clear()
        client.cookies.set(name=AuthManager.cookie_name, value=self.BAD_TOKEN)
        response = client.get(self.ME_URL)
        assert response.status_code == 401

    @reset_database
    def test_expired_token(self) -> None:
        client.post(self.SIGNUP_URL, json=self.TEST_PAYLOAD)
        time.sleep(3)
        response = client.get(self.ME_URL)
        assert response.status_code == 401
