from openapi_server.apis.draw_results_api_base import BaseDrawResultsApi
from openapi_server.models.draw_result import DrawResult


class DrawResultsApiImpl(BaseDrawResultsApi):
    """
    Получение результатов жеребьёвки.
    """

    _topics_db = {}
    _draw_results_db = {}

    async def draw_results_get(
        self,
        sectionId: int,
    ) -> list[DrawResult]:
        results = self._draw_results_db.get(sectionId, [])

        draw_results = []
        for result in results:
            topics_info = []
            for topic in result["topics"]:
                topic_data = self._topics_db.get(topic["topic_id"])
                if topic_data:
                    topics_info.append(
                        {
                            "topic_id": topic_data["id"],
                            "topic_name": topic_data["name"],
                        }
                    )

            if topics_info:
                draw_results.append(
                    DrawResult(
                        group_id=result["group_id"],
                        group_name=result["group_name"],
                        topics=topics_info,
                    )
                )

        return draw_results
