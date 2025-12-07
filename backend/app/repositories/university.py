from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import University
from app.schemas import UniversityCreate


class UniversityRepository:
    """Data access layer for universities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_universities(self) -> Sequence[University]:
        stmt = select(University).order_by(University.name)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def create_university(self, data: UniversityCreate) -> University:
        university = University(name=data.name)
        self._session.add(university)
        await self._session.flush()
        return university
