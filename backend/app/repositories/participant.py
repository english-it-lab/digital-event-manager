from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Participant


class ParticipantRepository:
    """Data access layer for participants."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_participant_by_id(self, participant_id: int) -> Participant | None:
        """
        Retrieve a participant by ID.

        Args:
            participant_id: ID of the participant

        Returns:
            Participant instance or None if not found
        """
        stmt = select(Participant).where(Participant.id == participant_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
