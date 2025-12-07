from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.university import UniversityRepository
from app.services.university import UniversityService


async def get_session() -> AsyncIterator[AsyncSession]:
    async for session in get_db_session():
        yield session


def get_university_service(
    session: AsyncSession = Depends(get_session),
) -> UniversityService:
    repository = UniversityRepository(session)
    return UniversityService(repository)
