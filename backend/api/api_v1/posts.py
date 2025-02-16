from typing import List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from core.schemas.post import PostList, PostCreate, PostSingle
from crud import posts as posts_services

router = APIRouter(
    prefix=settings.api.v1.posts,
    tags=["Posts"],
)


@router.get("/", response_model=List[PostList])
async def get_posts(
        # session: AsyncSession = Depends(db_helper.session_getter),
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
):
    users = await posts_services.get_post_list(session=session)
    return users


@router.post("/", status_code=201, response_model=PostSingle)
async def create_post(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        post_create: PostCreate
):
    user = await posts_services.create_post(
        session=session,
        post_create=post_create,
    )
    return user
