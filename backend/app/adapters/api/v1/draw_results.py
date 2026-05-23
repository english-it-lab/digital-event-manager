from openapi_server.apis.draw_results_api_base import BaseDrawResultsApi
from openapi_server.models.draw_result import DrawResult

from app.db.session import get_db_session
from app.repositories.group import GroupRepository
from app.repositories.group_topic import GroupTopicRepository
from app.repositories.topic import TopicRepository
from app.services.draw import DrawService


class DrawResultsApiImpl(BaseDrawResultsApi):
    """
    Получение результатов жеребьёвки.
    """

    async def draw_results_get(
        self,
        sectionId: int,
    ) -> list[DrawResult]:
        async for session in get_db_session():
            topic_repo = TopicRepository(session)
            group_repo = GroupRepository(session)
            group_topic_repo = GroupTopicRepository(session)

            service = DrawService(topic_repo, group_repo, group_topic_repo)
            results = await service.get_results(sectionId)
            return [
                DrawResult(group_id=r["group_id"], group_name=r["group_name"], topics=r["topics"]) for r in results
            ]
