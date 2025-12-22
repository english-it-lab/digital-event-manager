import random
from openapi_server.apis.draw_api_base import BaseDrawApi
import typing
from app.services.topic import TopicService
from openapi_server.apis.topics_api import topics_get
from app.repositories.topic import TopicRepository
from app.services.topic import TopicService
from fastapi import HTTPException
from app.services.draw import DrawService
from app.db.session import get_db_session
from app.repositories.section import SectionRepository

class DrawApiImpl(BaseDrawApi):
    """
    Реализация запуска жеребьёвки.
    """

    #_topics_db = {}
    #_draw_results_db = {}

    async def _with_service(self) -> DrawService:
       # создаём сессию для каждого вызова
       async for session in get_db_session():
           topic_repo = TopicRepository(session)
           sec_repo = SectionRepository(session)
           service = DrawService(sec_repo, topic_repo)
           yield service

    async def draw_run_post(
        self,
        sectionId: int,
    ) -> None:
        async for service in self._with_service():
            result = await service.draw_topics(self, sectionId)
            if result== "Недостаточно групп или тем":
                raise HTTPException(409, "Нет тем для распределения в секции")
            elif result == "Секция не найдена":
                raise HTTPException(404, "Секция не найдена")
            elif result == "Val err":
                raise HTTPException(422, "Validation error")
            else:
                return "Жеребьёвка выполнена"


