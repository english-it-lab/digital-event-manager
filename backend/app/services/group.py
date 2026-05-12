from collections.abc import Sequence
from typing import Literal

from app.enums.group import GroupStatus
from app.models import Group
from app.repositories.group import GroupRepository
from app.repositories.section import SectionRepository
from app.schemas import GroupCreate, GroupFilter, GroupUpdate


class GroupService:
    def __init__(
        self,
        repository: GroupRepository,
        section_repository: SectionRepository,
    ) -> None:
        self._repository = repository
        self._section_repository = section_repository

    async def list_groups(self, filters: GroupFilter) -> Sequence[Group]:
        return await self._repository.list_groups(filters)

    async def get_group_by_id(self, group_id: int) -> Group | None:
        return await self._repository.get_group_by_id(group_id)

    async def create_group(self, payload: GroupCreate) -> Group | Literal["SECTION_NOT_FOUND"]:
        section_id, name = payload.section_id, payload.name

        if not await self._section_exists(section_id):
            return "SECTION_NOT_FOUND"

        return await self._repository.create_group(section_id, name)

    async def update_group(self, group_id: int, payload: GroupUpdate) -> Group | None:
        group = await self._repository.get_group_by_id(group_id)

        if group is None:
            return None

        return await self._repository.update_group(group, payload)

    async def delete_group(self, group_id: int) -> bool:
        group = await self._repository.get_group_by_id(group_id)

        if group is None:
            return False

        await self._repository.delete_group(group)
        return True

    async def submit_group(self, group_id: int) -> Group | Literal["NOT_FOUND", "TRANSITION_ERROR"]:
        group = await self._repository.get_group_by_id(group_id)

        if group is None:
            return "NOT_FOUND"

        if group.status != GroupStatus.FORMING:
            return "TRANSITION_ERROR"

        group = await self._repository.update_status(group, GroupStatus.PENDING)
        return group

    async def approve_group(self, group_id: int) -> Group | Literal["NOT_FOUND", "TRANSITION_ERROR"]:
        group = await self._repository.get_group_by_id(group_id)

        if group is None:
            return "NOT_FOUND"

        if group.status != GroupStatus.PENDING:
            return "TRANSITION_ERROR"

        group = await self._repository.update_status(group, GroupStatus.APPROVED)
        return group

    async def reject_group(self, group_id: int) -> Group | Literal["NOT_FOUND", "TRANSITION_ERROR"]:
        group = await self._repository.get_group_by_id(group_id)

        if group is None:
            return "NOT_FOUND"

        if group.status != GroupStatus.PENDING:
            return "TRANSITION_ERROR"

        group = await self._repository.update_status(group, GroupStatus.REJECTED)
        return group

    async def _section_exists(self, section_id: int) -> bool:
        section = await self._section_repository.get_section_by_id(section_id)
        return section is not None
