from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from sqladmin import Admin

from src.admin import AdminAuth, ItemAdmin, UserAdmin
from src.core.config import settings
from src.core.database import engine
from src.core.trace import tracer_provider
from src.logging import configure_logging, default_logging_config
from src.middlewares import LoggingMiddleware
from src.urls import router

configure_logging()

app = FastAPI()

app.include_router(router)

# Add middleware to the app
app.add_middleware(LoggingMiddleware)

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer_provider)

origins = [
    settings.server_url,
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.main:app",
        access_log=False,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_config=default_logging_config(),
    )
