from collections.abc import Sequence

from fastapi import HTTPException, status

from app.models import Group
from app.repositories.group import GroupRepository
from app.repositories.section import SectionRepository
from app.schemas import GroupCreate, GroupUpdate


class GroupService:
    """Business logic for group entities."""

    def __init__(
        self,
        repository: GroupRepository,
        section_repository: SectionRepository,
    ) -> None:
        self._repository = repository
        self._section_repository = section_repository

    async def list_groups(self, skip: int = 0, limit: int = 100) -> Sequence[Group]:
        return await self._repository.list_groups(skip, limit)

    async def list_by_section(self, section_id: int) -> Sequence[Group]:
        return await self._repository.list_by_section(section_id)

    async def get_group_by_id(self, group_id: int) -> Group:
        group = await self._repository.get_group_by_id(group_id)
        if group is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group {group_id} not found")
        return group

    async def create_group(self, data: GroupCreate) -> Group:
        if data.name is None or len(data.name) == 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Group name cannot be empty")

        if data.section_id:
            section = await self._section_repository.get_section_by_id(data.section_id)
            if section is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f"Section {data.section_id} not found"
                )

        return await self._repository.create_group(data)

    async def update_group(self, group_id: int, data: GroupUpdate) -> Group:
        group = await self._repository.update_group(group_id, data)
        if group is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group {group_id} not found")
        return group

    async def delete_group(self, group_id: int) -> None:
        if not await self._repository.delete_group(group_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Group {group_id} not found")
