from collections.abc import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Group
from app.schemas import GroupCreate, GroupUpdate
from datetime import datetime


class GroupRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_groups(self, skip: int = 0, limit: int = 100) -> Sequence[Group]:
        stmt = select(Group).order_by(Group.id).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def list_by_section(self, section_id: int) -> Sequence[Group]:
        stmt = select(Group).where(Group.section_id == section_id)
        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def get_group_by_id(self, group_id: int) -> Group | None:
        stmt = select(Group).where(Group.id == group_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_group(self, data: GroupCreate) -> Group:
        group = Group(**data.model_dump(), registration_time=datetime.now())
        self._session.add(group)
        await self._session.commit()
        await self._session.refresh(group)
        return group

    async def update_group(self, group_id: int, data: GroupUpdate) -> Group | None:
        group = await self.get_group_by_id(group_id)
        if not group:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(group, key, value)

        await self._session.commit()
        await self._session.refresh(group)
        return group

    async def delete_group(self, group_id: int) -> bool:
        group = await self.get_group_by_id(group_id)
        if not group:
            return False
        await self._session.delete(group)
        await self._session.commit()
        return True
