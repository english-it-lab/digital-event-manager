# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field  # noqa: F401
from typing import Any, List  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.draw_result import DrawResult  # noqa: F401
from openapi_server.models.topic import Topic  # noqa: F401
from openapi_server.models.topic_create import TopicCreate  # noqa: F401
from openapi_server.models.topic_update import TopicUpdate  # noqa: F401


def test_sections_section_id_topics_get(client: TestClient):
    """Test case for sections_section_id_topics_get

    Получить список тем для секции
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/sections/{sectionId}/topics".format(sectionId=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_sections_section_id_topics_post(client: TestClient):
    """Test case for sections_section_id_topics_post

    Создать новую тему для секции
    """
    topic_create = {"name":"name"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/sections/{sectionId}/topics".format(sectionId=56),
    #    headers=headers,
    #    json=topic_create,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_topics_topic_id_get(client: TestClient):
    """Test case for topics_topic_id_get

    Получить тему по ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/topics/{topicId}".format(topicId=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_topics_topic_id_put(client: TestClient):
    """Test case for topics_topic_id_put

    Обновить тему
    """
    topic_update = {"section_id":1,"name":"name"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/topics/{topicId}".format(topicId=56),
    #    headers=headers,
    #    json=topic_update,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_topics_topic_id_delete(client: TestClient):
    """Test case for topics_topic_id_delete

    Удалить тему
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/topics/{topicId}".format(topicId=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_sections_section_id_draw_results_get(client: TestClient):
    """Test case for sections_section_id_draw_results_get

    Получить результаты жеребьёвки (распределение тем по группам)
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/sections/{sectionId}/draw/results".format(sectionId=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_sections_section_id_draw_run_post(client: TestClient):
    """Test case for sections_section_id_draw_run_post

    Запустить жеребьёвку (распределить темы секции по группам)
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/sections/{sectionId}/draw/run".format(sectionId=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

