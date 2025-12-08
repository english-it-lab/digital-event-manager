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
