"""
Dependencies for event program generation (separate to avoid circular imports)
"""
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.event import EventRepository
from app.repositories.section import SectionRepository
from app.repositories.participant import ParticipantRepository
from app.services.event_program import EventProgramService
from app.services.pdf_generator import PDFGeneratorService

# Импортируем базовую зависимость сессии из основного файла
from .dependencies import get_session

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