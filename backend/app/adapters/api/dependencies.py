from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.poster_content import PosterContentRepository
from app.repositories.technical_requirement import (
    TechnicalRequirementRepository,
)
from app.repositories.topic import TopicRepository
from app.repositories.university import UniversityRepository
from app.services.poster_content import PosterContentService
from app.services.technical_requirement import TechnicalRequirementService
from app.services.university import UniversityService


async def get_session() -> AsyncIterator[AsyncSession]:
    async for session in get_db_session():
        yield session


def get_university_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UniversityService:
    repository = UniversityRepository(session)
    return UniversityService(repository)


def get_technical_requirement_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TechnicalRequirementService:
    repository = TechnicalRequirementRepository(session)
    topic_repository = TopicRepository(session)
    return TechnicalRequirementService(repository, topic_repository)


def get_poster_content_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PosterContentService:
    repository = PosterContentRepository(session)
    tech_req_repository = TechnicalRequirementRepository(session)
    return PosterContentService(repository, tech_req_repository)
