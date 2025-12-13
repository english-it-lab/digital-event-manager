from openapi_server.apis.draw_api_base import BaseDrawApi
from openapi_server.models.draw_result import DrawResult
from openapi_server.models.topic import Topic
from openapi_server.models.topic_create import TopicCreate
from openapi_server.models.topic_update import TopicUpdate


class DrawApiImpl(BaseDrawApi):
    """
    Реализация Draw API поверх бизнес-логики приложения.
    """

    # Временное хранилище (замените на базу данных)
    _topics_db = {}
    _next_id = 1
    _draw_results_db = {}

    async def sections_section_id_topics_get(
        self,
        sectionId: int,
    ) -> list[Topic]:
        """
        Получить список тем для секции
        """
        # Фильтруем темы по section_id
        section_topics = [topic for topic in self._topics_db.values() if topic["section_id"] == sectionId]

        # Преобразуем в модель Topic
        return [
            Topic(
                id=topic["id"],
                section_id=topic["section_id"],
                name=topic["name"],
            )
            for topic in section_topics
        ]

    async def sections_section_id_topics_post(
        self,
        sectionId: int,
        topic_create: TopicCreate,
    ) -> Topic:
        """
        Создать новую тему для секции
        """
        # Валидация - проверяем, что имя не пустое
        if not topic_create.name or len(topic_create.name.strip()) < 3:
            from fastapi import HTTPException

            raise HTTPException(
                status_code=400,
                detail="Название темы должно содержать минимум 3 символа",
            )

        # Создаём новую тему
        new_topic = {
            "id": self._next_id,
            "section_id": sectionId,
            "name": topic_create.name.strip(),
        }

        # Сохраняем
        self._topics_db[self._next_id] = new_topic
        self._next_id += 1

        # Возвращаем модель
        return Topic(
            id=new_topic["id"],
            section_id=new_topic["section_id"],
            name=new_topic["name"],
        )

    async def topics_topic_id_get(
        self,
        topicId: int,
    ) -> Topic:
        """
        Получить тему по ID
        """
        # Ищем тему
        topic = self._topics_db.get(topicId)
        if not topic:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail=f"Тема с ID {topicId} не найдена")

        # Возвращаем модель
        return Topic(id=topic["id"], section_id=topic["section_id"], name=topic["name"])

    async def topics_topic_id_put(
        self,
        topicId: int,
        topic_update: TopicUpdate,
    ) -> Topic:
        """
        Обновить тему
        """
        # Проверяем существование темы
        if topicId not in self._topics_db:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail=f"Тема с ID {topicId} не найдена")

        # Получаем текущую тему
        topic = self._topics_db[topicId]

        # Обновляем поля
        if topic_update.name is not None:
            if len(topic_update.name.strip()) < 3:
                from fastapi import HTTPException

                raise HTTPException(
                    status_code=400,
                    detail="Название темы должно содержать минимум 3 символа",
                )
            topic["name"] = topic_update.name.strip()

        if topic_update.section_id is not None:
            topic["section_id"] = topic_update.section_id

        # Сохраняем
        self._topics_db[topicId] = topic

        # Возвращаем обновлённую модель
        return Topic(id=topic["id"], section_id=topic["section_id"], name=topic["name"])

    async def topics_topic_id_delete(
        self,
        topicId: int,
    ) -> None:
        """
        Удалить тему
        """
        # Проверяем существование темы
        if topicId not in self._topics_db:
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail=f"Тема с ID {topicId} не найдена")

        # TODO: Проверка на назначение теме группе
        # if self._is_topic_assigned(topicId):
        #     raise HTTPException(
        #         status_code=409,
        #         detail="Нельзя удалить тему — она уже назначена группе"
        #     )

        # Удаляем тему
        del self._topics_db[topicId]

        # Удаляем из результатов жеребьёвки, если есть
        for section_id, results in list(self._draw_results_db.items()):
            self._draw_results_db[section_id] = [
                result for result in results if any(topic["topic_id"] != topicId for topic in result["topics"])
            ]

    async def sections_section_id_draw_results_get(
        self,
        sectionId: int,
    ) -> list[DrawResult]:
        """
        Получить результаты жеребьёвки (распределение тем по группам)
        """
        # Получаем результаты для секции
        results = self._draw_results_db.get(sectionId, [])

        # Преобразуем в модели DrawResult
        draw_results = []
        for result in results:
            # Получаем информацию о теме
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

            # Создаём DrawResult только если есть темы
            if topics_info:
                draw_results.append(
                    DrawResult(
                        group_id=result["group_id"],
                        group_name=result["group_name"],
                        topics=topics_info,
                    )
                )

        return draw_results

    async def sections_section_id_draw_run_post(
        self,
        sectionId: int,
    ) -> None:
        """
        Запустить жеребьёвку (распределить темы секции по группам)
        """
        # Получаем все темы секции
        section_topics = [topic for topic in self._topics_db.values() if topic["section_id"] == sectionId]

        if not section_topics:
            from fastapi import HTTPException

            raise HTTPException(status_code=409, detail="Нет тем для распределения в секции")

        # TODO: Получить список групп для секции (заглушка)
        groups = [
            {"id": 1, "name": "Группа 1"},
            {"id": 2, "name": "Группа 2"},
            {"id": 3, "name": "Группа 3"},
        ]

        if len(groups) < len(section_topics):
            from fastapi import HTTPException

            raise HTTPException(
                status_code=409,
                detail=f"Недостаточно групп ({len(groups)}) для распределения {len(section_topics)} тем",
            )

        # Простой алгоритм распределения: каждая тема - одной группе
        import random

        # Перемешиваем темы
        shuffled_topics = section_topics.copy()
        random.shuffle(shuffled_topics)

        # Распределяем
        results = []
        for i, topic in enumerate(shuffled_topics):
            if i < len(groups):
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

        # Сохраняем результаты
        self._draw_results_db[sectionId] = results
