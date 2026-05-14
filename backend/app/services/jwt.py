from datetime import UTC, datetime, timedelta

from jose import jwt

from app.core.config import settings


class JwtService:
    """Business logic for JWT tokens."""

    ALGORITHM = "HS256"

    def create_jwt(self, data: dict, ttl_minutes: int) -> str:
        payload = data.copy()
        print(timedelta(minutes=ttl_minutes))
        print(datetime.now(UTC) + timedelta(minutes=ttl_minutes))
        payload["exp"] = datetime.now(UTC) + timedelta(minutes=ttl_minutes)
        return jwt.encode(payload, settings.jwt_secret_key, algorithm=self.ALGORITHM)

    def decode_jwt(self, token: str) -> dict:
        return jwt.decode(token, settings.jwt_secret_key, algorithms=[self.ALGORITHM])
