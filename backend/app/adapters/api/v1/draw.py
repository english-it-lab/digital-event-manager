import random
from openapi_server.apis.draw_api_base import BaseDrawApi
import typing
from backend.app.services.topic import TopicService
from backend.openapi_server.apis.topics_api import topics_get
from app.repositories.topic import TopicRepository
from app.services.topic import TopicService
from fastapi import HTTPException

class DrawApiImpl(BaseDrawApi):
    """
    Реализация запуска жеребьёвки.
    """

    _topics_db = {}
    _draw_results_db = {}

    async def _with_service(self) -> DrawService:
        # создаём сессию для каждого вызова
        async for session in get_db_session():
            repo = TopicRepository(session)
            top_service = TopicService(repo)
            service = DrawService()
            yield service

    async def draw_run_post(
        self,
        sectionId: int,
    ) -> None:
        async for service in self._with_service():
            result = await service.draw_topics(sectionId)
            if result== "Недостаточно групп или тем":
                raise HTTPException(409, "Нет тем для распределения в секции")
            elif result == "Секция не найдена":
                raise HTTPException(404, "Секция не найдена")
            elif result == "Val err":
                raise HTTPException(422, "Validation error")
            else:
                return "Жеребьёвка выполнена"


