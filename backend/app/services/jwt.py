from jose import jwt

from app.core.config import settings


class JwtService:
    """Business logic for JWT tokens."""

    ALGORITHM = "HS256"

    def create_jwt(self, data: dict) -> str:
        return jwt.encode(data, settings.jwt_secret_key, algorithm=self.ALGORITHM)

    def decode_jwt(self, token: str) -> dict:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[self.ALGORITHM])
