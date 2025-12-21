from fastapi import HTTPException

from app.models import Topic
from app.repositories.topic import TopicRepository

from openapi_server.models.topic_create import TopicCreate
from openapi_server.models.topic_update import TopicUpdate


class TopicService:
    def __init__(self, topic_repo: TopicRepository):
        self._topic_repo = topic_repo

    async def list_topics(self, section_id: int) -> list[Topic]:
        return await self._topic_repo.list_by_section(section_id)

    async def get_topic(self, topic_id: int) -> Topic:
        topic = await self._topic_repo.get_topic_by_id(topic_id)
        if not topic:
            raise HTTPException(404, "Тема не найдена")
        return topic

    async def create_topic(self, section_id: int, payload: TopicCreate) -> Topic:
        if len(payload.name.strip()) < 3:
            raise HTTPException(400, "Название темы минимум 3 символа")

        return await self._topic_repo.create(section_id, payload)

    async def update_topic(self, topic_id: int, payload: TopicUpdate) -> Topic:
        topic = await self._topic_repo.get_topic_by_id(topic_id)
        if not topic:
            raise HTTPException(404, "Тема не найдена")

        if payload.name is not None and len(payload.name.strip()) < 3:
            raise HTTPException(400, "Название темы минимум 3 символа")

        return await self._topic_repo.update(topic, payload)

    async def delete_topic(self, topic_id: int) -> None:
        topic = await self._topic_repo.get_topic_by_id(topic_id)
        if not topic:
            raise HTTPException(404, "Тема не найдена")

        await self._topic_repo.delete(topic)
