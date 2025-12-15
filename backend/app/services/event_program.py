# app/services/event_program.py
from collections.abc import Sequence
from app.models import Event, Section, Participant
from app.repositories.event import EventRepository
from app.repositories.section import SectionRepository
from app.repositories.participant import ParticipantRepository

class EventProgramService:
    def __init__(
        self,
        event_repo: EventRepository,
        section_repo: SectionRepository,
        participant_repo: ParticipantRepository,
    ):
        self._event_repo = event_repo
        self._section_repo = section_repo
        self._participant_repo = participant_repo
    
    async def get_event_program_data(self, event_id: int) -> dict:
        # 1. Получаем мероприятие с организатором
        event = await self._event_repo.get_event_with_organizer(event_id)
        if not event:
            raise ValueError(f"Мероприятие {event_id} не найдено")
        
        # 2. Получаем все секции мероприятия
        sections = await self._section_repo.get_sections_by_event(event_id)
        
        # 3. Для каждой секции получаем участников
        sections_data = []
        for section in sections:
            participants = await self._participant_repo.get_participants_by_section(section.id)
            
            # Формируем данные участника
            participants_data = []
            for participant in participants:
                person = participant.person
                participants_data.append({
                    "id": participant.id,
                    "full_name": f"{person.last_name} {person.first_name} {person.middle_name or ''}".strip(),
                    "university": participant.faculty.university.name if participant.faculty else "",
                    "faculty": participant.faculty.name if participant.faculty else "",
                    "presentation_topic": participant.presentation_topic,
                    "is_poster": participant.is_poster_participant,
                })
            
            sections_data.append({
                "id": section.id,
                "name": section.name,
                "lecture_hall": section.lecture_hall,
                "time": section.time,
                "participants": participants_data,
            })
        
        # 4. Формируем итоговую структуру
        return {
            "event": {
                "id": event.id,
                "name": event.name,
                "type": event.type,
                "date": event.date,
                "venue": {
                    "city": event.venue.city,
                    "street": event.venue.street,
                    "building": event.venue.building,
                } if event.venue else {},
                "organizer": {
                    "full_name": f"{event.organizer.person.last_name} {event.organizer.person.first_name}",
                    "contact": event.organizer.contact_number,
                } if event.organizer else {},
            },
            "sections": sections_data,
        }