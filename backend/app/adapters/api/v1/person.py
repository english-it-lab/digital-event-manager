from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.adapters.api.dependencies import get_person_service
from app.adapters.api.v1.AuthAdapter import get_jwt_payload_dep
from app.schemas import PersonRead, PersonUpdate
from app.services.jwt import AuthPayload
from app.services.person import PersonService

router = APIRouter(tags=["person"])


@router.put("/", response_model=PersonRead, status_code=status.HTTP_200_OK)
async def put_person(
    payload: PersonUpdate,
    service: Annotated[PersonService, Depends(get_person_service)],
    auth_payload: Annotated[AuthPayload, Depends(get_jwt_payload_dep)],
) -> PersonRead:
    return await service.put_person(auth_payload.PERSON_ID, payload)


@router.post("/", response_model=PersonRead, status_code=status.HTTP_200_OK)
async def create_person(
    payload: PersonUpdate,
    service: Annotated[PersonService, Depends(get_person_service)],
    auth_payload: Annotated[AuthPayload, Depends(get_jwt_payload_dep)],
) -> PersonRead:
    return await service.create_person(auth_payload.PERSON_ID, payload)


@router.patch("/", response_model=PersonRead, status_code=status.HTTP_200_OK)
async def update_person(
    payload: PersonUpdate,
    service: Annotated[PersonService, Depends(get_person_service)],
    auth_payload: Annotated[AuthPayload, Depends(get_jwt_payload_dep)],
) -> PersonRead:
    return await service.update_person(auth_payload.PERSON_ID, payload)


@router.get("/", response_model=PersonRead, status_code=status.HTTP_200_OK)
async def get_person_by_id(payload: int, service: Annotated[PersonService, Depends(get_person_service)]) -> PersonRead:
    return await service.get_person_by_id(payload)


@router.get("/me", response_model=PersonRead, status_code=status.HTTP_200_OK)
async def get_person_data_from_jwt(
    service: Annotated[PersonService, Depends(get_person_service)],
    auth_payload: Annotated[AuthPayload, Depends(get_jwt_payload_dep)],
) -> PersonRead:
    return await service.get_person_by_id(auth_payload.PERSON_ID)
