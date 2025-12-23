
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.section import SectionRepository
from app.repositories.topic import TopicRepository
from app.models import Group
from app.db.session import get_db_session
from random import random



class DrawService:
    def __init__(self,
        section_repository: SectionRepository,
        topic_repository: TopicRepository) -> None:
        self._section_repository = section_repository
        self._topic_repository = topic_repository


    async def draw_topics(self, db: AsyncSession, section_id: int):

        section = await self._section_repository.get_section_by_id(section_id)
        print("Section id: {section_id}, section: {section}")
        if section is None:
            return "Секция не найдена"

        section_topics = await self._topic_repository.list_by_section(section_id)

        if not section_topics:
            return "Недостаточно групп или тем"

        session = get_db_session()
        stmt = select(Group).where(Group.section_id == section_id)
        res = await self._session.execute(stmt)
        groups = res.scalars().all()

        if len(groups) < len(section_topics):
           return "Недосточно групп или тем"

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

        self._draw_results_db[section_id] = results


