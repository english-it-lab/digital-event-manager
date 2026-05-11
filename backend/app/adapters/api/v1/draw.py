import random
from openapi_server.apis.draw_api_base import BaseDrawApi
from fastapi import HTTPException
from app.db.session import get_db_session
from app.repositories.topic import TopicRepository
from app.repositories.group import GroupRepository
from app.repositories.group_topic import GroupTopicRepository
from app.services.draw import DrawService


class DrawApiImpl(BaseDrawApi):
    """
    Реализация запуска жеребьёвки.
    """

    # _draw_results_db = {}

    async def draw_run_post(
        self,
        sectionId: int,
    ) -> None:
        async for session in get_db_session():
            topic_repo = TopicRepository(session)
            group_repo = GroupRepository(session)
            group_topic_repo = GroupTopicRepository(session)

            service = DrawService(topic_repo, group_repo, group_topic_repo)

            await service.run_draw(sectionId)  # results
            # Сохраняем в памяти (для обратной совместимости)
            # self._draw_results_db[sectionId] = results
