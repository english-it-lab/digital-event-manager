from collections.abc import Sequence

from app.models import Person
from app.repositories.person import PersonRepository
from app.schemas import PersonCreate


class PersonService:
    """Business logic for people."""

    def __init__(self, repository: PersonRepository) -> None:
        self._repository = repository

    async def list_people(self, skip: int = 0, limit: int = 100) -> Sequence[Person]:
        return await self._repository.list_people(skip, limit)

    async def get_person(self, person_id: int) -> Person | None:
        return await self._repository.get_person_by_id(person_id)

    async def create_person(self, payload: PersonCreate) -> Person:
        return await self._repository.create_person(payload)

    async def update_person(self, person_id: int, payload: PersonCreate) -> Person:
        person = await self._repository.get_person_by_id(person_id)
        if not person:
            raise ValueError(f"Человек {person_id} не найден")
        return await self._repository.update_person(person, payload)

    async def delete_person(self, person_id: int) -> None:
        person = await self._repository.get_person_by_id(person_id)
        if not person:
            raise ValueError(f"Человек {person_id} не найден")
        await self._repository.delete_person(person)
