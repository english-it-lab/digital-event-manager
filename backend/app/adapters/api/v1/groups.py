from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.adapters.api.dependencies import get_group_service
from app.models import Group
from app.schemas import GroupCreate, GroupFilter, GroupRead, GroupUpdate
from app.services.group import GroupService

router = APIRouter(tags=["groups"])


@router.get("/", response_model=list[GroupRead])
async def list_groups(
    params: Annotated[GroupFilter, Query()],
    service: Annotated[GroupService, Depends(get_group_service)],
) -> list[GroupRead]:
    groups = await service.list_groups(params)
    return [GroupRead.model_validate(group) for group in groups]


@router.get("/{group_id}", response_model=GroupRead)
async def get_group(
    group_id: int,
    service: Annotated[GroupService, Depends(get_group_service)],
) -> GroupRead:
    group = await service.get_group_by_id(group_id)

    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found",
        )

    return GroupRead.model_validate(group)


@router.post("/", response_model=GroupRead, status_code=status.HTTP_201_CREATED)
async def create_group(
    payload: GroupCreate,
    service: Annotated[GroupService, Depends(get_group_service)],
) -> GroupRead:
    result = await service.create_group(payload)

    match result:
        case Group() as group:
            return GroupRead.model_validate(group)

        case "SECTION_NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Section with id {payload.section_id} not found"
            )


@router.patch("/", response_model=GroupRead)
async def update_group(
    group_id: int,
    payload: GroupUpdate,
    service: Annotated[GroupService, Depends(get_group_service)]
) -> GroupRead:
    group = await service.update_group(group_id, payload)

    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} is not found",
        )

    return GroupRead.model_validate(group)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_group(
    group_id: int,
    service: Annotated[GroupService, Depends(get_group_service)],
) -> None:
    group = await service.delete_group(group_id)

    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with id {group_id} not found",
        )


@router.post("/{group_id}/submit")
async def submit_group(
    group_id: int,
    service: Annotated[GroupService, Depends(get_group_service)],
) -> GroupRead:
    result = await service.submit_group(group_id)

    match result:
        case Group() as group:
            return GroupRead.model_validate(group)

        case "NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id} not found"
            )

        case "TRANSITION_ERROR":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Group status must be FORMING"
            )


@router.post("/{group_id}/approve")
async def approve_group(
    group_id: int,
    service: Annotated[GroupService, Depends(get_group_service)],
) -> GroupRead:
    result = await service.approve_group(group_id)

    match result:
        case Group() as group:
            return GroupRead.model_validate(group)

        case "NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id} not found"
            )

        case "TRANSITION_ERROR":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Group status must be PENDING"
            )


@router.post("/{group_id}/reject")
async def reject_group(
    group_id: int,
    service: Annotated[GroupService, Depends(get_group_service)],
) -> GroupRead:
    result = await service.reject_group(group_id)

    match result:
        case Group() as group:
            return GroupRead.model_validate(group)

        case "NOT_FOUND":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Group with id {group_id} not found"
            )

        case "TRANSITION_ERROR":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Group status must be PENDING"
            )
