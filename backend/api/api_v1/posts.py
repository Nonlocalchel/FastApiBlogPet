from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.fastapi_users import current_active_user
from core.config import settings
from core.models import db_helper, User
from core.schemas.post import PostList, PostCreate, PostSingle
from crud import posts as posts_services

router = APIRouter(
    prefix=settings.api.v1.posts,
    tags=["Posts"],
)


@router.get("/", response_model=List[PostList])
async def get_posts(
        session: AsyncSession = Depends(db_helper.session_getter),
        # session: Annotated[
        #     AsyncSession,
        #     Depends(db_helper.session_getter),
        # ],
):
    users = await posts_services.get_post_list(session=session)
    return users


@router.get("/{pk}", response_model=PostSingle)
async def post_single(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        pk: int
):
    post = await posts_services.get_post(post_id=pk, session=session)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", status_code=201, response_model=PostSingle)
async def create_post(
        session: Annotated[
            AsyncSession,
            Depends(db_helper.session_getter),
        ],
        post_create: PostCreate,
        user: User = Depends(current_active_user)
):
    post = await posts_services.create_post(
        session=session,
        post_create=post_create,
    )
    return post
