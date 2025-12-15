from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Section, EventSection

class SectionRepository:
    """Data access layer for sections."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def get_sections_by_event(self, event_id: int) -> Sequence[Section]:
        stmt = (
            select(Section)
            .join(EventSection, Section.id == EventSection.section_id)
            .where(EventSection.event_id == event_id)
            .order_by(Section.time)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()