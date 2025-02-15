from fastapi import APIRouter

from core.config import settings

from .auth import router as users_router

router = APIRouter()
router.include_router(
    users_router
)
