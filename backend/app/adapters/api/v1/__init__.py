from fastapi import APIRouter

from app.adapters.api.v1 import (
    poster_contents,
    technical_requirements,
    universities,
    events,
)

router = APIRouter()
router.include_router(universities.router, prefix="/universities")
router.include_router(events.router,prefix="/events")
router.include_router(
    technical_requirements.router, prefix="/technical-requirements"
)
router.include_router(poster_contents.router, prefix="/poster-contents")
