from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqladmin import Admin

from src.admin import AdminAuth, ItemAdmin, UserAdmin
from src.core.database import engine
from src.urls import router

app = FastAPI()

app.include_router(router)

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

add_pagination(app)

authentication_backend = AdminAuth(secret_key="")
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(ItemAdmin)
