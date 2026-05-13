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

    async def get_person_by_email(self, email: str) -> Person | None:
        stmt = select(Person).where(Person.email == email)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_person(self, email: str) -> Person:
        person = Person(email=email)

        self._session.add(person)

        await self._session.flush()
        await self._session.refresh(person)
        return person
