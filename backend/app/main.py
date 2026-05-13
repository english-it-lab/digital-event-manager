from fastapi import FastAPI

from app.adapters.api.swagger import configure_openapi
from app.adapters.api.v1 import router as api_v1_router
from app.core.config import settings


def create_app() -> FastAPI:
    application = FastAPI(title=settings.app_name)
    application.include_router(api_v1_router, prefix=settings.api_v1_prefix)
    configure_openapi(application)
    return application


app = create_app()
