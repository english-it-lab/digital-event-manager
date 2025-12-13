from openapi_server.apis.topics_api_base import BaseTopicsApi
from openapi_server.models.topic import Topic
from openapi_server.models.topic_create import TopicCreate
from openapi_server.models.topic_update import TopicUpdate


class TopicsApiImpl(BaseTopicsApi):
    """
    Реализация Topics API (CRUD тем).
    """

    _topics_db = {}
    _next_id = 1
    _draw_results_db = {}

    async def topics_get(
        self,
        sectionId: int,
    ) -> list[Topic]:
        section_topics = [topic for topic in self._topics_db.values() if topic["section_id"] == sectionId]

        return [Topic(**topic) for topic in section_topics]

    async def topics_post(
        self,
        sectionId: int,
        topic_create: TopicCreate,
    ) -> Topic:
        if not topic_create.name or len(topic_create.name.strip()) < 3:
            from fastapi import HTTPException

            raise HTTPException(400, "Название темы должно содержать минимум 3 символа")

        new_topic = {
            "id": self._next_id,
            "section_id": sectionId,
            "name": topic_create.name.strip(),
        }

        self._topics_db[self._next_id] = new_topic
        self._next_id += 1

        return Topic(**new_topic)

    async def topics_topic_id_get(
        self,
        topicId: int,
    ) -> Topic:
        topic = self._topics_db.get(topicId)
        if not topic:
            from fastapi import HTTPException

            raise HTTPException(404, f"Тема с ID {topicId} не найдена")

        return Topic(**topic)

    async def topics_topic_id_put(
        self,
        topicId: int,
        topic_update: TopicUpdate,
    ) -> Topic:
        topic = self._topics_db.get(topicId)
        if not topic:
            from fastapi import HTTPException

            raise HTTPException(404, f"Тема с ID {topicId} не найдена")

        if topic_update.name is not None:
            if len(topic_update.name.strip()) < 3:
                from fastapi import HTTPException

                raise HTTPException(400, "Название темы должно содержать минимум 3 символа")
            topic["name"] = topic_update.name.strip()

        if topic_update.section_id is not None:
            topic["section_id"] = topic_update.section_id

        self._topics_db[topicId] = topic
        return Topic(**topic)

    async def topics_topic_id_delete(
        self,
        topicId: int,
    ) -> None:
        if topicId not in self._topics_db:
            from fastapi import HTTPException

            raise HTTPException(404, f"Тема с ID {topicId} не найдена")

        del self._topics_db[topicId]

        for section_id, results in self._draw_results_db.items():
            self._draw_results_db[section_id] = [
                r for r in results if all(t["topic_id"] != topicId for t in r["topics"])
            ]
