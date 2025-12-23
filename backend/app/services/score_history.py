from app.repositories.score_history import ScoreHistoryRepository
from app.models import ScoreHistory


from typing import Sequence


class ScoreHistoryService:
    def __init__(
        self,
        score_history_repo: ScoreHistoryRepository,
    ):
        self.score_history_repo = score_history_repo

    async def get_all_history(self) -> Sequence[ScoreHistory]:
        return await self.score_history_repo.get_all()

    async def create_history_entry(
        self,
        jury_score_id: int,
        jury_id: int | None,
        old_score: float | None,
        new_score: float | None,
    ) -> ScoreHistory:
        return await self.score_history_repo.create(
            jury_score_id=jury_score_id,
            jury_id=jury_id,
            old_score=old_score,
            new_score=new_score,
        )
