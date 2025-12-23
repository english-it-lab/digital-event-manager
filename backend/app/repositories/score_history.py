from sqlalchemy.ext.asyncio import AsyncSession
from app.models import ScoreHistory
from sqlalchemy import select
from typing import Sequence


class ScoreHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        jury_score_id: int,
        jury_id: int | None,
        old_score: float | None,
        new_score: float | None,
    ) -> ScoreHistory:
        history = ScoreHistory(
            jury_score_id=jury_score_id,
            jury_id=jury_id,
            old_score=old_score,
            new_score=new_score,
        )
        self.session.add(history)
        await self.session.flush()
        return history

    async def get_all(self) -> Sequence[ScoreHistory]:
        stmt = select(ScoreHistory).order_by(
            ScoreHistory.changed_at.desc()
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
