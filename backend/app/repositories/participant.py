from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Participant, Person, Faculty, University

class ParticipantRepository:
    """Data access layer for participants."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def get_participants_by_section(self, section_id: int) -> Sequence[Participant]:
        stmt = (
            select(Participant)
            .join(Person, Participant.person_id == Person.id)
            .join(Faculty, Participant.faculty_id == Faculty.id)
            .join(University, Faculty.university_id == University.id)
            .where(Participant.section_id == section_id)
            .order_by(Person.last_name, Person.first_name)
        )
        result = await self._session.execute(stmt)
        return result.scalars().all()