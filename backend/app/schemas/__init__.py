from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, constr


class ORMModelMixin:
    """Mixin that enables ORM mode for Pydantic models."""

    model_config = ConfigDict(from_attributes=True)


class UniversityBase(BaseModel):
    name: constr(max_length=255)


class UniversityCreate(UniversityBase):
    pass


class UniversityRead(ORMModelMixin, UniversityBase):
    id: int


class FacultyBase(BaseModel):
    university_id: int | None = None
    name: str


class FacultyCreate(FacultyBase):
    pass


class FacultyRead(ORMModelMixin, FacultyBase):
    id: int


class DepartmentBase(BaseModel):
    name: str


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentRead(ORMModelMixin, DepartmentBase):
    id: int


class PersonBase(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: str | None = None
    email: str | None = None
    title: str | None = None
    degree: str | None = None
    position: str | None = None
    workplace: str | None = None
    tg_name: str | None = None


class PersonCreate(PersonBase):
    pass


class PersonRead(ORMModelMixin, PersonBase):
    id: int


class OrganizerBase(BaseModel):
    person_id: int | None = None
    contact_number: str | None = None
    access_key: int | None = None


class OrganizerCreate(OrganizerBase):
    pass


class OrganizerRead(ORMModelMixin, OrganizerBase):
    id: int


class VenueBase(BaseModel):
    city: str | None = None
    street: str | None = None
    building: str | None = None


class VenueCreate(VenueBase):
    pass


class VenueRead(ORMModelMixin, VenueBase):
    id: int


class EventBase(BaseModel):
    venue_id: int | None = None
    organizer_id: int | None = None
    name: str | None = None
    type: str | None = None
    event_date: date | None = None


class EventCreate(EventBase):
    pass


class EventRead(ORMModelMixin, EventBase):
    id: int


class CourseBase(BaseModel):
    year: int | None = None


class CourseCreate(CourseBase):
    pass


class CourseRead(ORMModelMixin, CourseBase):
    id: int


class TextbookLevelBase(BaseModel):
    level_abbreviation: str | None = None


class TextbookLevelCreate(TextbookLevelBase):
    pass


class TextbookLevelRead(ORMModelMixin, TextbookLevelBase):
    id: int


class SectionBase(BaseModel):
    name: str
    lecture_hall: str | None = None
    time: datetime | None = None


class SectionCreate(SectionBase):
    pass


class SectionRead(ORMModelMixin, SectionBase):
    id: int


class EventSectionBase(BaseModel):
    event_id: int
    section_id: int


class EventSectionCreate(EventSectionBase):
    pass


class EventSectionRead(ORMModelMixin, EventSectionBase):
    id: int


class TopicBase(BaseModel):
    section_id: int | None = None
    name: str | None = None


class TopicCreate(TopicBase):
    pass


class TopicRead(ORMModelMixin, TopicBase):
    id: int


class GroupBase(BaseModel):
    section_id: int | None = None
    name: str | None = None
    member_count: int | None = None
    registration_time: datetime | None = None


class GroupCreate(GroupBase):
    pass


class GroupRead(ORMModelMixin, GroupBase):
    id: int


class GroupTopicBase(BaseModel):
    group_id: int
    topic_id: int | None = None


class GroupTopicCreate(GroupTopicBase):
    pass


class GroupTopicRead(ORMModelMixin, GroupTopicBase):
    id: int


class TeacherBase(BaseModel):
    university_id: int | None = None
    department_id: int | None = None
    person_id: int | None = None


class TeacherCreate(TeacherBase):
    pass


class TeacherRead(ORMModelMixin, TeacherBase):
    id: int


class ParticipantBase(BaseModel):
    person_id: int | None = None
    faculty_id: int | None = None
    course_id: int | None = None
    teacher_id: int | None = None
    section_id: int | None = None
    is_poster_participant: bool = Field(default=False)
    is_translator_participant: bool = Field(default=False)
    has_translator_education: bool = Field(default=False)
    textbook_level_id: int | None = None
    is_group_leader: bool = Field(default=False)
    presentation_topic: str | None = None
    is_notification_allowed: bool = Field(default=True)
    password_hash: str | None = None


class ParticipantCreate(ParticipantBase):
    pass


class ParticipantRead(ORMModelMixin, ParticipantBase):
    id: int


class GroupParticipantBase(BaseModel):
    group_id: int
    participant_id: int


class GroupParticipantCreate(GroupParticipantBase):
    pass


class GroupParticipantRead(ORMModelMixin, GroupParticipantBase):
    id: int


class JuryBase(BaseModel):
    university_id: int | None = None
    person_id: int | None = None
    is_chairman: bool = Field(default=False)
    access_key: int | None = None


class JuryCreate(JuryBase):
    pass


class JuryRead(ORMModelMixin, JuryBase):
    id: int


class SectionJuryBase(BaseModel):
    section_id: int
    jury_id: int


class SectionJuryCreate(SectionJuryBase):
    pass


class SectionJuryRead(ORMModelMixin, SectionJuryBase):
    id: int


class JuryScoreBase(BaseModel):
    jury_id: int | None = None
    participant_id: int | None = None
    organization_score: float | None = None
    content: float | None = None
    visuals: float | None = None
    mechanics: float | None = None
    delivery: float | None = None
    comment: str | None = None


class JuryScoreCreate(JuryScoreBase):
    pass


class JuryScoreRead(ORMModelMixin, JuryScoreBase):
    id: int


class JuryScoreChangeBase(BaseModel):
    jury_scores_id: int
    jury_id: int | None = None
    update_time: datetime | None = None


class JuryScoreChangeCreate(JuryScoreChangeBase):
    pass


class JuryScoreChangeRead(ORMModelMixin, JuryScoreChangeBase):
    id: int


class OrganizerSectionChangeBase(BaseModel):
    section_id: int
    organizer_id: int | None = None
    update_time: datetime | None = None


class OrganizerSectionChangeCreate(OrganizerSectionChangeBase):
    pass


class OrganizerSectionChangeRead(ORMModelMixin, OrganizerSectionChangeBase):
    id: int


class OrganizerParticipantChangeBase(BaseModel):
    participant_id: int
    organizer_id: int | None = None
    update_time: datetime | None = None


class OrganizerParticipantChangeCreate(OrganizerParticipantChangeBase):
    pass


class OrganizerParticipantChangeRead(ORMModelMixin, OrganizerParticipantChangeBase):
    id: int


class TechnicalRequirementBase(BaseModel):
    topic_id: int | None = None
    format: str | None = None
    sizes: str | None = None


class TechnicalRequirementCreate(TechnicalRequirementBase):
    pass


class TechnicalRequirementRead(ORMModelMixin, TechnicalRequirementBase):
    id: int


class PosterContentBase(BaseModel):
    technical_requirements_id: int | None = None
    words_amount: int | None = None
    images_amount: int | None = None


class PosterContentCreate(PosterContentBase):
    pass


class PosterContentRead(ORMModelMixin, PosterContentBase):
    id: int


__all__ = [
    "ORMModelMixin",
    "UniversityBase",
    "UniversityCreate",
    "UniversityRead",
    "FacultyBase",
    "FacultyCreate",
    "FacultyRead",
    "DepartmentBase",
    "DepartmentCreate",
    "DepartmentRead",
    "PersonBase",
    "PersonCreate",
    "PersonRead",
    "OrganizerBase",
    "OrganizerCreate",
    "OrganizerRead",
    "VenueBase",
    "VenueCreate",
    "VenueRead",
    "EventBase",
    "EventCreate",
    "EventRead",
    "CourseBase",
    "CourseCreate",
    "CourseRead",
    "TextbookLevelBase",
    "TextbookLevelCreate",
    "TextbookLevelRead",
    "SectionBase",
    "SectionCreate",
    "SectionRead",
    "EventSectionBase",
    "EventSectionCreate",
    "EventSectionRead",
    "TopicBase",
    "TopicCreate",
    "TopicRead",
    "GroupBase",
    "GroupCreate",
    "GroupRead",
    "GroupTopicBase",
    "GroupTopicCreate",
    "GroupTopicRead",
    "TeacherBase",
    "TeacherCreate",
    "TeacherRead",
    "ParticipantBase",
    "ParticipantCreate",
    "ParticipantRead",
    "GroupParticipantBase",
    "GroupParticipantCreate",
    "GroupParticipantRead",
    "JuryBase",
    "JuryCreate",
    "JuryRead",
    "SectionJuryBase",
    "SectionJuryCreate",
    "SectionJuryRead",
    "JuryScoreBase",
    "JuryScoreCreate",
    "JuryScoreRead",
    "JuryScoreChangeBase",
    "JuryScoreChangeCreate",
    "JuryScoreChangeRead",
    "OrganizerSectionChangeBase",
    "OrganizerSectionChangeCreate",
    "OrganizerSectionChangeRead",
    "OrganizerParticipantChangeBase",
    "OrganizerParticipantChangeCreate",
    "OrganizerParticipantChangeRead",
    "TechnicalRequirementBase",
    "TechnicalRequirementCreate",
    "TechnicalRequirementRead",
    "PosterContentBase",
    "PosterContentCreate",
    "PosterContentRead",
]
