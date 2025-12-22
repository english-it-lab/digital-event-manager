# app/repositories/__init__.py
from .events import EventRepository
from .section import SectionRepository
from .participant import ParticipantRepository
from .poster_content import PosterContentRepository
from .technical_requirement import TechnicalRequirementRepository
from .topic import TopicRepository
from .university import UniversityRepository

__all__ = [
    "EventRepository",
    "SectionRepository",
    "ParticipantRepository",
    "PosterContentRepository",
    "TechnicalRequirementRepository",
    "TopicRepository",
    "UniversityRepository",
]