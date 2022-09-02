from fastapi import FastAPI

from app.api import settings
from app.core import config, tasks
from app.api.routes import router as api_router


def get_application():
    application = FastAPI(
        title=settings.project_name,
        version=settings.version,
        debug=settings.debug
    )

    application.include_router(api_router, prefix="/api")

    application.add_event_handler("startup", tasks.create_start_app_handler(application))
    application.add_event_handler("shutdown", tasks.create_stop_app_handler(application))

    return application


app = get_application()
