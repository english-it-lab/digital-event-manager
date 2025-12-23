from openapi_server.apis.draw_api_base import BaseDrawApi


class DrawApiImpl(BaseDrawApi):
    """
    Реализация запуска жеребьёвки.
    """

    _topics_db = {}
    _draw_results_db = {}

    async def draw_run_post(
        self,
        sectionId: int,
    ) -> None:
        section_topics = [topic for topic in self._topics_db.values() if topic["section_id"] == sectionId]

        if not section_topics:
            from fastapi import HTTPException

            raise HTTPException(409, "Нет тем для распределения в секции")

        groups = [
            {"id": 1, "name": "Группа 1"},
            {"id": 2, "name": "Группа 2"},
            {"id": 3, "name": "Группа 3"},
        ]

        if len(groups) < len(section_topics):
            from fastapi import HTTPException

            raise HTTPException(
                409,
                f"Недостаточно групп ({len(groups)}) для {len(section_topics)} тем",
            )

        import random

        random.shuffle(section_topics)

        results = []
        for i, topic in enumerate(section_topics):
            group = groups[i]
            results.append(
                {
                    "group_id": group["id"],
                    "group_name": group["name"],
                    "topics": [
                        {
                            "topic_id": topic["id"],
                            "topic_name": topic["name"],
                        }
                    ],
                }
            )

        self._draw_results_db[sectionId] = results
