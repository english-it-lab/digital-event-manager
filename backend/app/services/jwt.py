from jose import jwt

from app.core.config import settings
from app.schemas import AuthPayload


class JwtService:
    """Business logic for JWT tokens."""

    ALGORITHM = "HS256"

    async def create_jwt(self, auth_payload: AuthPayload) -> str:
        return jwt.encode(auth_payload.model_dump(), settings.jwt_secret_key, algorithm=self.ALGORITHM)

    async def decode_jwt(self, token: str) -> AuthPayload:
        return AuthPayload.model_validate(jwt.decode(token, settings.jwt_secret_key, algorithms=[self.ALGORITHM]))
