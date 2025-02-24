from fastapi_users.authentication import JWTStrategy
from core.config import settings

SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=settings.access_token.lifetime_seconds)
