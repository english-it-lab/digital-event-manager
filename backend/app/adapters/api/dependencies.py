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

"""
Dependencies for event program generation (separate to avoid circular imports)
"""
from app.repositories.events import EventRepository
from app.repositories.section import SectionRepository
from app.repositories.participant import ParticipantRepository
from app.services.events import EventProgramService
from app.services.pdf_generator import PDFGeneratorService

from app.repositories.venues import VenueRepository
from app.services.venues import VenuesService


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


def get_event_program_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EventProgramService:
    """Dependency for event program service."""
    event_repo = EventRepository(session)
    section_repo = SectionRepository(session)
    participant_repo = ParticipantRepository(session)
    return EventProgramService(event_repo, section_repo, participant_repo)

def get_pdf_generator_service() -> PDFGeneratorService:
    """Dependency for PDF generator service."""
    return PDFGeneratorService()

def get_venues(
    session: Annotated[AsyncSession, Depends(get_session)],
)-> VenuesService:
    repository = VenueRepository(session)
    return VenuesService(repository)
