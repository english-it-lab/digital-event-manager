from fastapi import APIRouter

from app.adapters.api.v1 import (
    juries,
    participant_scores,
    poster_contents,
    technical_requirements,
    universities,
)
from app.adapters.api.v1.draw import DrawApiImpl
from app.adapters.api.v1.draw_results import DrawResultsApiImpl
from app.adapters.api.v1.topics import TopicsApiImpl
from openapi_server.apis.draw_api import router as draw_router
from openapi_server.apis.draw_results_api import router as draw_results_router
from openapi_server.apis.topics_api import router as topics_router

router = APIRouter()
router.include_router(universities.router, prefix="/universities")
router.include_router(technical_requirements.router, prefix="/technical-requirements")
router.include_router(poster_contents.router, prefix="/poster-contents")
router.include_router(juries.router, prefix="/juries")
router.include_router(participant_scores.router, prefix="/participants/{participant_id}/scores")
router.include_router(draw_router)
router.include_router(draw_results_router)
router.include_router(topics_router)
