from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.event import EventRepository
from app.repositories.jury import JuryRepository
from app.repositories.jury_score import JuryScoreRepository
from app.repositories.organizer import OrganizerRepository
from app.repositories.participant import ParticipantRepository
from app.repositories.person import PersonRepository
from app.repositories.poster_content import PosterContentRepository
from app.repositories.section import SectionRepository
from app.repositories.section_jury import SectionJuryRepository
from app.repositories.technical_requirement import (
    TechnicalRequirementRepository,
)
from app.repositories.topic import TopicRepository
from app.repositories.university import UniversityRepository
from app.services.jury import JuryService
from app.services.jury_score import JuryScoreService
from app.services.poster_content import PosterContentService
from app.services.section import SectionService
from app.services.technical_requirement import TechnicalRequirementService
from app.services.university import UniversityService
from app.services.topic import TopicService


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


def get_jury_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> JuryService:
    jury_repository = JuryRepository(session)
    university_repository = UniversityRepository(session)
    person_repository = PersonRepository(session)
    return JuryService(
        jury_repository=jury_repository,
        university_repository=university_repository,
        person_repository=person_repository,
    )


def get_jury_score_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> JuryScoreService:
    """Dependency injection for JuryScoreService."""
    jury_score_repo = JuryScoreRepository(session)
    participant_repo = ParticipantRepository(session)
    jury_repo = JuryRepository(session)
    section_jury_repo = SectionJuryRepository(session)

    return JuryScoreService(
        jury_score_repository=jury_score_repo,
        participant_repository=participant_repo,
        jury_repository=jury_repo,
        section_jury_repository=section_jury_repo,
    )


def get_section_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SectionService:
    repository = SectionRepository(session)
    organizer_repository = OrganizerRepository(session)
    event_repository = EventRepository(session)
    return SectionService(repository, organizer_repository, event_repository)

def get_topic_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> TopicService:
    topic_repository = TopicRepository(session)
    return TopicService(topic_repository)
