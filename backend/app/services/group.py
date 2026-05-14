from collections.abc import Sequence
from typing import Literal

from app.enums.group import GroupStatus
from app.models import Group
from app.repositories.group import GroupRepository
from app.repositories.organizer import OrganizerRepository
from app.repositories.section import SectionRepository
from app.schemas import GroupCreate, GroupFilter, GroupUpdate


class GroupService:
    def __init__(
        self,
        repository: GroupRepository,
        organizer_repository: OrganizerRepository,
        section_repository: SectionRepository,
    ) -> None:
        self._repository = repository
        self._organizer_repository = organizer_repository
        self._section_repository = section_repository

    async def list_groups(self, filters: GroupFilter) -> Sequence[Group]:
        return await self._repository.list_groups(filters)

    async def get_group_by_id(self, group_id: int) -> Group | None:
        return await self._repository.get_group_by_id(group_id)

    async def create_group(self, user_id: int, payload: GroupCreate) -> Group | Literal["SECTION_NOT_FOUND"]:
        section_id, name = payload.section_id, payload.name

        if not await self._section_exists(section_id):
            return "SECTION_NOT_FOUND"

        return await self._repository.create_group(section_id, name)

    async def update_group(self, user_id: int, group_id: int, payload: GroupUpdate) -> Group | Literal["NOT_FOUND", "NOT_LEADER"]:
        group = await self._repository.get_group_by_id(group_id)

        if group is None:
            return "NOT_FOUND"

        if not self._repository.is_leader(group_id, user_id):
            return "NOT_LEADER"

        return await self._repository.update_group(group, payload)

    async def delete_group(self, user_id: int, group_id: int) -> Literal["GOOD", "NOT_FOUND", "NOT_LEADER"]:
        group = await self._repository.get_group_by_id(group_id)

        if group is None:
            return "NOT_FOUND"

        if not self._repository.is_leader(group_id, user_id):
            return "NOT_LEADER"

        await self._repository.delete_group(group)
        return "GOOD"

    async def submit_group(self, user_id: int, group_id: int) -> Group | Literal["NOT_FOUND", "NOT_LEADER", "TRANSITION_ERROR"]:
        group = await self._repository.get_group_by_id(group_id)

        if group is None:
            return "NOT_FOUND"

        if not self._repository.is_leader(group_id, user_id):
            return "NOT_LEADER"

        if group.status != GroupStatus.FORMING:
            return "TRANSITION_ERROR"

        group = await self._repository.update_status(group, GroupStatus.PENDING)
        group = await self._repository.set_registration_time(group)
        return group

    async def approve_group(self, user_id: int, group_id: int) -> Group | Literal["NOT_ORGANIZER", "NOT_FOUND", "TRANSITION_ERROR"]:
        if not self._organizer_repository.exists_by_id(user_id):
            return "NOT_ORGANIZER"

        group = await self._repository.get_group_by_id(group_id)

        if group is None:
            return "NOT_FOUND"

        if group.status != GroupStatus.PENDING:
            return "TRANSITION_ERROR"

        group = await self._repository.update_status(group, GroupStatus.APPROVED)
        return group

    async def reject_group(self, user_id: int, group_id: int) -> Group | Literal["NOT_ORGANIZER", "NOT_FOUND", "TRANSITION_ERROR"]:
        if not self._organizer_repository.exists_by_id(user_id):
            return "NOT_ORGANIZER"

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