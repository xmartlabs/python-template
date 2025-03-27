from fastapi import Request
from fastapi.responses import RedirectResponse
from sqladmin import ModelView
from sqladmin.authentication import AuthenticationBackend

from src.core.database import async_session_generator
from src.core.security import AuthManager, PasswordManager
from src.models import Item, User


class AdminAuth(AuthenticationBackend):
    cookie_name = "admin-cookie"

    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        async_session = async_session_generator()
        async with async_session() as session:
            user = await User.objects(session).get(User.email == email)
            await session.refresh(user)
        if not user or not user.is_superuser:
            return False
        if not PasswordManager.verify_password(password, user.password):  # type: ignore[arg-type]
            return False
        token, _ = AuthManager.create_access_token(user=user)
        request.session.update({AdminAuth.cookie_name: token})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        failed_auth_response = RedirectResponse(
            request.url_for("admin:login"), status_code=302
        )
        manager = AuthManager()
        token = request.session.get(AdminAuth.cookie_name)
        if not token:
            return failed_auth_response
        try:
            async_session = async_session_generator()
            async with async_session() as session:
                user = await manager.get_user_from_token(token=token, session=session)
                await session.refresh(user)
        except Exception:
            return failed_auth_response
        finally:
            await session.close()
        if not user.is_superuser:
            return failed_auth_response
        return True


class UserAdmin(ModelView, model=User):
    column_list = [
        User.email,
        User.created_at,
        User.id,
    ]
    column_searchable_list = [User.id, User.email]


class ItemAdmin(ModelView, model=Item):
    column_list = [
        Item.name,
        Item.description,
        Item.is_public,
        Item.owner,
        Item.created_at,
        Item.id,
    ]
