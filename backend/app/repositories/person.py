from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Person
from app.schemas import PersonCreate


class PersonRepository:
    """Data access layer for people."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_people(self, skip: int = 0, limit: int = 100) -> Sequence[Person]:
        stmt = select(Person).order_by(Person.last_name, Person.first_name).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_person_by_id(self, person_id: int) -> Person | None:
        stmt = select(Person).where(Person.id == person_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_person(self, data: PersonCreate) -> Person:
        person = Person(
            first_name=data.first_name,
            last_name=data.last_name,
            middle_name=data.middle_name,
            email=data.email,
            title=data.title,
            degree=data.degree,
            position=data.position,
            workplace=data.workplace,
            tg_name=data.tg_name,
        )
        self._session.add(person)
        await self._session.commit()
        await self._session.refresh(person)
        return person

    async def update_person(self, person: Person, data: PersonCreate) -> Person:
        person.first_name = data.first_name
        person.last_name = data.last_name
        person.middle_name = data.middle_name
        person.email = data.email
        person.title = data.title
        person.degree = data.degree
        person.position = data.position
        person.workplace = data.workplace
        person.tg_name = data.tg_name
        await self._session.commit()
        await self._session.refresh(person)
        return person

    async def delete_person(self, person: Person) -> None:
        await self._session.delete(person)
        await self._session.commit()
