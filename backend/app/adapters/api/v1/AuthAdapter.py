import time
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.adapters.api.dependencies import get_jwt_service
from app.services.jwt import AuthPayload, JwtService

bearer = HTTPBearer(auto_error=False)


async def get_jwt_payload_dep(
    creds: Annotated[HTTPAuthorizationCredentials, Depends(bearer)],
    jwt_service: Annotated[JwtService, Depends(get_jwt_service)],
) -> AuthPayload:
    if not creds or creds.scheme.lower() != "bearer":
        raise HTTPException(401, "missing token")
    try:
        payload = await jwt_service.decode_jwt(creds.credentials)
    except Exception:
        raise HTTPException(401, "invalid token") from None
    if time.time() > payload.EXPIRATION_DATE:
        raise HTTPException(401, "token expired")
    return payload
