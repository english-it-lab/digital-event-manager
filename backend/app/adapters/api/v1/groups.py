from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.adapters.api.dependencies import get_group_service
from app.schemas import GroupCreate, GroupRead, GroupUpdate
from app.services.group import GroupService

router = APIRouter(tags=["Groups"])


@router.get("/", response_model=list[GroupRead])
async def read_groups(
    service: Annotated[GroupService, Depends(get_group_service)], skip: int = 0, limit: int = 100
) -> list[GroupRead]:
    groups = await service.list_groups(skip, limit)
    return [GroupRead.model_validate(g) for g in groups]


@router.get("/by-section/{section_id}", response_model=list[GroupRead])
async def read_groups_by_section(
    section_id: int, service: Annotated[GroupService, Depends(get_group_service)]
) -> list[GroupRead]:
    groups = await service.list_by_section(section_id)
    return [GroupRead.model_validate(g) for g in groups]


@router.get("/{group_id}", response_model=GroupRead)
async def read_group(group_id: int, service: Annotated[GroupService, Depends(get_group_service)]) -> GroupRead:
    return GroupRead.model_validate(await service.get_group_by_id(group_id))


@router.post("/", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
async def create_group(data: GroupCreate, service: Annotated[GroupService, Depends(get_group_service)]) -> GroupRead:
    return GroupRead.model_validate(await service.create_group(data))


@router.patch("/{group_id}", response_model=GroupRead)
async def update_group(
    group_id: int, data: GroupUpdate, service: Annotated[GroupService, Depends(get_group_service)]
) -> GroupRead:
    return GroupRead.model_validate(await service.update_group(group_id, data))


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(group_id: int, service: Annotated[GroupService, Depends(get_group_service)]) -> None:
    await service.delete_group(group_id)
