from openapi_server.models.topic_create import TopicCreate
from openapi_server.models.topic_update import TopicUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Topic


class TopicRepository:
    """Data access layer for topics."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_topic_by_id(self, topic_id: int) -> Topic | None:
        """
        Retrieve a topic by ID.

        Args:
            topic_id: ID of the topic

        Returns:
            Topic instance or None if not found
        """
        stmt = select(Topic).where(Topic.id == topic_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_section(self, section_id: int) -> list[Topic]:
        stmt = select(Topic).where(Topic.section_id == section_id)
        res = await self._session.execute(stmt)
        return res.scalars().all()

    async def create(self, section_id: int, data: TopicCreate) -> Topic:
        topic = Topic(section_id=section_id, name=data.name.strip())
        self._session.add(topic)
        await self._session.flush()
        await self._session.refresh(topic)
        await self._session.commit()
        return topic

    async def update(self, topic: Topic, data: TopicUpdate) -> Topic:
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(topic, k, v)
        await self._session.flush()
        await self._session.refresh(topic)
        await self._session.commit()
        return topic

    async def delete(self, topic: Topic) -> None:
        await self._session.delete(topic)
        await self._session.flush()
        await self._session.commit()
