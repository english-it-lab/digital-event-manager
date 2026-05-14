from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.adapters.api.dependencies import get_jwt_service
from app.services.jwt import AuthPayload, JwtService

router = APIRouter(tags=["jwts"])


@router.post("/", response_model=str, status_code=status.HTTP_200_OK)
async def create_jwt(
    payload: AuthPayload,
    service: Annotated[JwtService, Depends(get_jwt_service)],
) -> str:
    return await service.create_jwt_from_payload(payload)


@router.get("/decode", response_model=dict, status_code=status.HTTP_200_OK)
async def decode_jwt(
    token: Annotated[str, Query(description="JWT for decoding")],
    service: Annotated[JwtService, Depends(get_jwt_service)],
) -> AuthPayload:
    return await service.decode_jwt(token)
