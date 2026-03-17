from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.adapters.api.dependencies import get_group_service
from app.schemas import GroupRead
from app.services.group import GroupService

router = APIRouter(tags=["groups"])


@router.patch("/{group_id}/register", response_model=GroupRead)
async def register_group_to_section(
    group_id: int,
    section_id: int,
    service: Annotated[GroupService, Depends(get_group_service)],
) -> GroupRead:
    group = await service.register_group_to_section(group_id, section_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found",
        )
    return GroupRead.model_validate(group)
