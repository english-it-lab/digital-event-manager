from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models import (
    EventSection,
    Group,
    GroupParticipant,
    GroupTopic,
    Participant,
    Section,
    TechnicalRequirement,
    Topic,
)


class NotificationRepository:
    def __init__(self, session):
        self._session = session

    async def get_notification_payload(self, event_id: int):
        stmt = (
            select(Group)
            .join(Section, Group.section_id == Section.id)
            .join(EventSection, EventSection.section_id == Section.id)
            .where(EventSection.event_id == event_id)
            .options(
                selectinload(Group.group_topics)
                .joinedload(GroupTopic.topic)
                .selectinload(Topic.technical_requirements)
                .joinedload(TechnicalRequirement.posters_content),
                selectinload(Group.group_participants)
                .joinedload(GroupParticipant.participant)
                .joinedload(Participant.person),
            )
        )

        result = await self._session.execute(stmt)
        return result.scalars().unique().all()
