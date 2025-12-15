from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Event, Organizer, Venue, Person

class EventRepository:
    """Data access layer for events."""
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
    
    async def get_event_with_organizer(self, event_id: int) -> Event:
        stmt = (
            select(Event)
            .join(Organizer, Event.organizer_id == Organizer.id)
            .join(Person, Organizer.person_id == Person.id)
            .join(Venue, Event.venue_id == Venue.id)
            .where(Event.id == event_id)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()