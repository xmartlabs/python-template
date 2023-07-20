from httpx import Response

from src.core.security import AuthManager, PasswordManager
from src.models import User
from src.tests.base import TestingSessionLocal, client, reset_database


class TestUser:
    SIGNUP_URL = "api/v1/users"
    LOGIN_URL = "api/v1/users/login"
    ME_URL = "api/v1/users/me"

    def check_user_token(self, email: str, password: str, token: str) -> None:
        """
        Checks that a user with the email and password provided was created in the DB,
        and that the token provided belongs to that user
        """
        with TestingSessionLocal() as session:
            user = User.objects(session).get(User.email == email)
            assert user is not None
            assert user.email == email
            assert PasswordManager.verify_password(password, user.password)
            assert user == AuthManager().get_user_from_token(token, session)

    def check_me_response(self, email: str, response: Response) -> None:
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == email
        assert data["is_active"] == True  # noqa: E712
        assert data["is_superuser"] == False  # noqa: E712

    @reset_database
    def test_signup(self) -> None:
        email = "test@test.com"
        password = "password"
        payload = {"email": email, "password": password}
        response = client.post(self.SIGNUP_URL, json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["token_type"] == "Bearer"
        token = data["access_token"]
        assert "expires_at" in data
        self.check_user_token(email=email, password=password, token=token)

    def test_signup_wrong_shema(self) -> None:
        response = client.post(self.SIGNUP_URL)
        assert response.status_code == 422

    @reset_database
    def test_signup_dup_emails(self) -> None:
        email = "test@test.com"
        payload = {"email": email, "password": "password"}
        client.post(self.SIGNUP_URL, json=payload)
        response = client.post(self.SIGNUP_URL, json=payload)
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Email address already in use"

    @reset_database
    def test_login(self) -> None:
        email = "test@test.com"
        password = "password"
        payload = {"email": email, "password": password}
        client.post(self.SIGNUP_URL, json=payload)
        response = client.post(self.LOGIN_URL, json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["token_type"] == "Bearer"
        token = data["access_token"]
        assert "expires_at" in data
        self.check_user_token(email=email, password=password, token=token)

    def test_login_wrong_shema(self) -> None:
        response = client.post(self.LOGIN_URL)
        assert response.status_code == 422

    @reset_database
    def test_login_fail(self) -> None:
        email = "test@test.com"
        password = "password"
        payload = {"email": email, "password": password}
        response = client.post(self.LOGIN_URL, json=payload)
        assert response.status_code == 401
        data = response.json()
        assert data["detail"] == "Invalid email or password"

    @reset_database
    def test_me_header(self) -> None:
        email = "test@test.com"
        payload = {"email": email, "password": "password"}
        sign_up_resp = client.post(self.SIGNUP_URL, json=payload)
        data = sign_up_resp.json()
        token = "Bearer " + data["access_token"]
        client.cookies.clear()
        response = client.get(self.ME_URL, headers={AuthManager.header_name: token})
        self.check_me_response(email=email, response=response)

    @reset_database
    def test_me_cookie(self) -> None:
        email = "test@test.com"
        payload = {"email": email, "password": "password"}
        client.post(self.SIGNUP_URL, json=payload)
        response = client.get(self.ME_URL)
        self.check_me_response(email=email, response=response)

    @reset_database
    def test_me_unauthenticated(self) -> None:
        response = client.get(self.ME_URL)
        assert response.status_code == 401
