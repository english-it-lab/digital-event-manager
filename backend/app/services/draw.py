
from sqlalchemy.ext.asyncio import AsyncSession

class DrawService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session


   async def draw_topics(self, db: AsyncSession)

       section_topics = topics_get(sectionId)

       if not section_topics:

       # Натуральная заглушка, пока никто не смог сделать нам CRUD для групп
       session = get_db_session()
       groups = [group for group in self..values() if topic["section_id"] == sectionId]

       if len(groups) < len(section_topics):
           from fastapi import HTTPException

           raise HTTPException(
               409,
               f"Недостаточно групп ({len(groups)}) для {len(section_topics)} тем",
           )

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


