from fastapi import APIRouter

from app.adapters.api.v1 import universities

router = APIRouter()
router.include_router(universities.router, prefix="/universities")
