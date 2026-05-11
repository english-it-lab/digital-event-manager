from fastapi import HTTPException
from app.repositories.topic import TopicRepository
from app.repositories.group import GroupRepository
from app.repositories.group_topic import GroupTopicRepository
import random
from pprint import pprint

class DrawService:
    """Service for draw logic."""

    def __init__(
        self,
        topic_repo: TopicRepository,
        group_repo: GroupRepository,
        group_topic_repo: GroupTopicRepository,
    ) -> None:
        self.topic_repo = topic_repo
        self.group_repo = group_repo
        self.group_topic_repo = group_topic_repo

    async def run_draw(self, section_id: int) -> dict:
        """Run draw for a section."""
        topics = await self.topic_repo.list_by_section(section_id)


        groups = await self.group_repo.list_by_section(section_id)

        if not topics:
            raise HTTPException(409, "Нет тем для распределения в секции")
        if not groups:
            raise HTTPException(409, "Нет групп для распределения в секции")

        shuffled = random.sample(topics, len(topics))
        num_topics = len(shuffled)
        num_groups = len(groups)

        results = []
        empty_groups = []  # список групп без тем
        topic_idx = 0

        if num_topics <= num_groups:
            for group in groups:
                if topic_idx < num_topics:
                    results.append({
                        "group_id": group.id,
                        "group_name": group.name,
                        "topics": [{
                            "topic_id": shuffled[topic_idx].id,
                            "topic_name": shuffled[topic_idx].name
                        }]
                    })
                    topic_idx += 1
                else:
                    results.append({
                        "group_id": group.id,
                        "group_name": group.name,
                        "topics": []
                    })
                    empty_groups.append({
                        "group_id": group.id,
                        "group_name": group.name
                    })
        else:
            base = num_topics // num_groups
            remainder = num_topics % num_groups

            for i, group in enumerate(groups):
                topics_count = base + (1 if i < remainder else 0)
                group_topics = []
                for _ in range(topics_count):
                    group_topics.append({
                        "topic_id": shuffled[topic_idx].id,
                        "topic_name": shuffled[topic_idx].name
                    })
                    topic_idx += 1
                results.append({
                    "group_id": group.id,
                    "group_name": group.name,
                    "topics": group_topics
                })

        await self.group_topic_repo.clear_section(section_id) # Чистим предыдущую жеребьевку
        for result in results:
            for topic in result["topics"]:
                await self.group_topic_repo.create(result["group_id"], topic["topic_id"])

        # Логируем пустые группы
        if empty_groups:
            print(f"[WARN] Секция {section_id}: группы без тем: {[g['group_name'] for g in empty_groups]}")
            # TODO: отправить уведомление организатору

        return {
            "section_id": section_id,
            "results": results,
            "empty_groups": empty_groups,
            "total_topics": num_topics,
            "total_groups": num_groups
        }
