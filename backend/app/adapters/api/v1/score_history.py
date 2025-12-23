from fastapi import APIRouter, Depends

from app.schemas import ScoreHistoryRead
from app.services.score_history import ScoreHistoryService
from app.adapters.api.dependencies import get_score_history_service


router = APIRouter(tags=["score-history"])

@router.get("/", response_model=list[ScoreHistoryRead])
async def get_all_score_history(
    service: ScoreHistoryService = Depends(get_score_history_service),
):
    history = await service.get_all_history()
    return history
