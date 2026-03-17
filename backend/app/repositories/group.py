from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Group
from app.schemas import GroupUpdate


class GroupRepository:
    """Data access layer for groups."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_group_by_id(self, group_id: int) -> Group | None:
        stmt = select(Group).where(Group.id == group_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update(self, group: Group, data: GroupUpdate) -> Group:
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(group, k, v)
        await self._session.flush()
        await self._session.refresh(group)
        await self._session.commit()
        return group
