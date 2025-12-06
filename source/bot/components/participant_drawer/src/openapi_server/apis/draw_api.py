# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.draw_api_base import BaseDrawApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field
from typing import Any, List
from typing_extensions import Annotated
from openapi_server.models.draw_result import DrawResult
from openapi_server.models.topic import Topic
from openapi_server.models.topic_create import TopicCreate
from openapi_server.models.topic_update import TopicUpdate


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/sections/{sectionId}/topics",
    responses={
        200: {"model": List[Topic], "description": "Список тем"},
    },
    tags=["Draw"],
    summary="Получить список тем для секции",
    response_model_by_alias=True,
)
async def sections_section_id_topics_get(
    sectionId: Annotated[int, Field(strict=True, ge=1)] = Path(..., description="", ge=1),
) -> List[Topic]:
    if not BaseDrawApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDrawApi.subclasses[0]().sections_section_id_topics_get(sectionId)


@router.post(
    "/sections/{sectionId}/topics",
    responses={
        201: {"model": Topic, "description": "Тема создана"},
        400: {"description": "Некорректные данные"},
        404: {"description": "Секция не найдена"},
    },
    tags=["Draw"],
    summary="Создать новую тему для секции",
    response_model_by_alias=True,
)
async def sections_section_id_topics_post(
    sectionId: Annotated[int, Field(strict=True, ge=1)] = Path(..., description="", ge=1),
    topic_create: TopicCreate = Body(None, description=""),
) -> Topic:
    if not BaseDrawApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDrawApi.subclasses[0]().sections_section_id_topics_post(sectionId, topic_create)


@router.get(
    "/topics/{topicId}",
    responses={
        200: {"model": Topic, "description": "Тема найдена"},
        404: {"description": "Тема не найдена"},
    },
    tags=["Draw"],
    summary="Получить тему по ID",
    response_model_by_alias=True,
)
async def topics_topic_id_get(
    topicId: Annotated[int, Field(strict=True, ge=1)] = Path(..., description="", ge=1),
) -> Topic:
    if not BaseDrawApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDrawApi.subclasses[0]().topics_topic_id_get(topicId)


@router.put(
    "/topics/{topicId}",
    responses={
        200: {"model": Topic, "description": "Тема обновлена"},
        400: {"description": "Некорректные данные"},
        409: {"description": "Нельзя обновить тему — она уже назначена группе"},
        404: {"description": "Тема не найдена"},
    },
    tags=["Draw"],
    summary="Обновить тему",
    response_model_by_alias=True,
)
async def topics_topic_id_put(
    topicId: Annotated[int, Field(strict=True, ge=1)] = Path(..., description="", ge=1),
    topic_update: TopicUpdate = Body(None, description=""),
) -> Topic:
    if not BaseDrawApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDrawApi.subclasses[0]().topics_topic_id_put(topicId, topic_update)


@router.delete(
    "/topics/{topicId}",
    responses={
        204: {"description": "Тема удалена"},
        409: {"description": "Нельзя удалить — тема уже назначена группе"},
        404: {"description": "Тема не найдена"},
    },
    tags=["Draw"],
    summary="Удалить тему",
    response_model_by_alias=True,
)
async def topics_topic_id_delete(
    topicId: Annotated[int, Field(strict=True, ge=1)] = Path(..., description="", ge=1),
) -> None:
    if not BaseDrawApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDrawApi.subclasses[0]().topics_topic_id_delete(topicId)


@router.get(
    "/sections/{sectionId}/draw/results",
    responses={
        200: {"model": List[DrawResult], "description": "Результаты распределения тем"},
        404: {"description": "Секция не найдена"},
    },
    tags=["Draw"],
    summary="Получить результаты жеребьёвки (распределение тем по группам)",
    response_model_by_alias=True,
)
async def sections_section_id_draw_results_get(
    sectionId: Annotated[int, Field(strict=True, ge=1)] = Path(..., description="", ge=1),
) -> List[DrawResult]:
    if not BaseDrawApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDrawApi.subclasses[0]().sections_section_id_draw_results_get(sectionId)


@router.post(
    "/sections/{sectionId}/draw/run",
    responses={
        200: {"description": "Темы секции распределены"},
        404: {"description": "Секция не найдена"},
        409: {"description": "Недостаточно групп и/или тем для распределения"},
    },
    tags=["Draw"],
    summary="Запустить жеребьёвку (распределить темы секции по группам)",
    response_model_by_alias=True,
)
async def sections_section_id_draw_run_post(
    sectionId: Annotated[int, Field(strict=True, ge=1)] = Path(..., description="", ge=1),
) -> None:
    if not BaseDrawApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseDrawApi.subclasses[0]().sections_section_id_draw_run_post(sectionId)
