from fastapi import FastAPI

from app import settings
from app.core import tasks
from app.api.routes import router as api_router
from app.core.models import HealthCheck


def get_application():
    application = FastAPI(
        title=settings.project_name,
        version=settings.version,
        debug=settings.debug
    )

    @application.get("/", response_model=HealthCheck, tags=["status"])
    async def health_check():
        return {
            "name": settings.project_name,
            "version": settings.version,
            "description": settings.description
        }

    application.include_router(api_router, prefix="/api")

    application.add_event_handler("startup", tasks.create_start_app_handler(application))
    application.add_event_handler("shutdown", tasks.create_stop_app_handler(application))

    return application


app = get_application()
