from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Organizer


class OrganizerRepository:
    """Data access layer for organizer management."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exists_by_id(self, organizer_id: int) -> bool:
        """Checks the existence of a record in the table."""
        stmt = select(exists().where(Organizer.id == organizer_id))
        return await self._session.scalar(stmt)
