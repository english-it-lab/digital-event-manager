from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import SectionJury


class SectionJuryRepository:
    """Data access layer for section-jury assignments."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def is_jury_assigned_to_section(self, jury_id: int, section_id: int) -> bool:
        """
        Check if a jury member is assigned to a specific section.

        Args:
            jury_id: ID of the jury member
            section_id: ID of the section

        Returns:
            True if assignment exists, False otherwise
        """
        stmt = select(SectionJury).where(SectionJury.jury_id == jury_id, SectionJury.section_id == section_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None
