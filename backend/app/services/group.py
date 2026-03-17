from collections.abc import Sequence

from fastapi import HTTPException, status

from app.models import Group
from app.repositories.group import GroupRepository
from app.repositories.section import SectionRepository
from app.schemas import GroupUpdate


class GroupService:
    """Business logic for university entities."""

    def __init__(self,
        group_repository: GroupRepository,
        section_repository: SectionRepository,
    ) -> None:
        self._group_repository = group_repository
        self._section_repository = section_repository

    async def register_group_to_section(self, group_id: int, section_id: int) -> Group:
        section = await self._section_repository.get_section_by_id(section_id)
        if section is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Section with id {section_id} not found",
            )

        group = await self._group_repository.get_group_by_id(group_id)
        if group is None:
            return None
        
        if group.section_id is not None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"The group is already registered to the section with id {group.section_id}",
            )

        return await self._group_repository.update(group=group, data=GroupUpdate(section_id=section_id))
