# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field
from typing import Any, List
from typing_extensions import Annotated
from openapi_server.models.draw_result import DrawResult
from openapi_server.models.topic import Topic
from openapi_server.models.topic_create import TopicCreate
from openapi_server.models.topic_update import TopicUpdate


class BaseDrawApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDrawApi.subclasses = BaseDrawApi.subclasses + (cls,)
    async def sections_section_id_topics_get(
        self,
        sectionId: Annotated[int, Field(strict=True, ge=1)],
    ) -> List[Topic]:
        ...


    async def sections_section_id_topics_post(
        self,
        sectionId: Annotated[int, Field(strict=True, ge=1)],
        topic_create: TopicCreate,
    ) -> Topic:
        ...


    async def topics_topic_id_get(
        self,
        topicId: Annotated[int, Field(strict=True, ge=1)],
    ) -> Topic:
        ...


    async def topics_topic_id_put(
        self,
        topicId: Annotated[int, Field(strict=True, ge=1)],
        topic_update: TopicUpdate,
    ) -> Topic:
        ...


    async def topics_topic_id_delete(
        self,
        topicId: Annotated[int, Field(strict=True, ge=1)],
    ) -> None:
        ...


    async def sections_section_id_draw_results_get(
        self,
        sectionId: Annotated[int, Field(strict=True, ge=1)],
    ) -> List[DrawResult]:
        ...


    async def sections_section_id_draw_run_post(
        self,
        sectionId: Annotated[int, Field(strict=True, ge=1)],
    ) -> None:
        ...
