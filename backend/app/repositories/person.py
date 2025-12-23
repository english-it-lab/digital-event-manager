from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Person


class PersonRepository:
    """Data access layer for people."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_person_by_id(self, person_id: int) -> Person | None:
        stmt = select(Person).where(Person.id == person_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
