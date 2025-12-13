from fastapi import APIRouter

from app.adapters.api.v1 import (
    poster_contents,
    technical_requirements,
    universities,
)
from app.adapters.api.v1.draw import DrawApiImpl
from openapi_server.apis.draw_api import router as draw_router

router = APIRouter()
router.include_router(universities.router, prefix="/universities")
router.include_router(technical_requirements.router, prefix="/technical-requirements")
router.include_router(poster_contents.router, prefix="/poster-contents")
router.include_router(draw_router, prefix="/api/v1")
