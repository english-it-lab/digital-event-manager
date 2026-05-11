from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.adapters.api.dependencies import get_jwt_service
from app.services.jwt import JwtService

router = APIRouter(tags=["jwts"])


@router.post("/", response_model=str, status_code=status.HTTP_200_OK)
async def create_jwt(
    payload: dict,
    service: Annotated[JwtService, Depends(get_jwt_service)],
) -> str:
    jwt_token = service.create_jwt(payload)
    return jwt_token


@router.get("/decode", response_model=dict, status_code=status.HTTP_200_OK)
async def decode_jwt(
    token: Annotated[str, Query(description="JWT for decoding")],
    service: Annotated[JwtService, Depends(get_jwt_service)],
) -> dict:
    try:
        decoded = service.decode_jwt(token)
        return decoded
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid token: {str(e)}",
        ) from e
