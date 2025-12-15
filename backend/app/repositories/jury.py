from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Jury


class JuryRepository:
    """Data access layer for jury members."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_jury_by_id(self, jury_id: int) -> Jury | None:
        """
        Retrieve a jury member by ID.

        Args:
            jury_id: ID of the jury member

        Returns:
            Jury instance or None if not found
        """
        stmt = select(Jury).where(Jury.id == jury_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
