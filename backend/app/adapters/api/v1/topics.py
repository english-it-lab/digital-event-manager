from openapi_server.apis.topics_api_base import BaseTopicsApi
from openapi_server.models.topic import Topic
from openapi_server.models.topic_create import TopicCreate
from openapi_server.models.topic_update import TopicUpdate

from app.db.session import get_db_session
from app.repositories.topic import TopicRepository
from app.services.topic import TopicService


class TopicsApiImpl(BaseTopicsApi):
    """
    Реализация Topics API (CRUD тем).
    """

    async def _with_service(self) -> TopicService:
        # создаём сессию для каждого вызова
        async for session in get_db_session():
            repo = TopicRepository(session)
            service = TopicService(repo)
            yield service

    async def topics_get(self, sectionId: int) -> list[Topic]:
        async for service in self._with_service():
            topics = await service.list_topics(sectionId)
            return [Topic(id=t.id, section_id=t.section_id, name=t.name) for t in topics]

    async def topics_post(self, sectionId: int, topic_create: TopicCreate) -> Topic:
        async for service in self._with_service():
            topic = await service.create_topic(sectionId, topic_create)
            return Topic(id=topic.id, section_id=topic.section_id, name=topic.name)

    async def topics_topic_id_get(self, topicId: int) -> Topic:
        async for service in self._with_service():
            topic = await service.get_topic(topicId)
            return Topic(id=topic.id, section_id=topic.section_id, name=topic.name)

    async def topics_topic_id_put(self, topicId: int, topic_update: TopicUpdate) -> Topic:
        async for service in self._with_service():
            topic = await service.update_topic(topicId, topic_update)
            return Topic(id=topic.id, section_id=topic.section_id, name=topic.name)

    async def topics_topic_id_delete(self, topicId: int) -> None:
        async for service in self._with_service():
            await service.delete_topic(topicId)
