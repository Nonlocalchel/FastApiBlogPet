from typing import List, Annotated

from fastapi import APIRouter, Depends, HTTPException
from api.api_v1.authentication.fastapi_users import current_active_user
from api.dependencies.unit_of_work import UOWDep
from core.config import settings
from core.models import User
from core.schemas.post import PostList, PostCreate, PostSingle
from services.posts import PostsService

router = APIRouter(
    prefix=settings.api.v1.posts,
    tags=["Posts"],
)


@router.get("/", response_model=List[PostList])
async def get_posts(
        uow: UOWDep,
):
    posts = await PostsService().get_posts(uow)
    return posts


@router.get("/{pk}", response_model=PostSingle)
async def post_single(
        uow: UOWDep,
        pk: int
):
    post = await PostsService().get_post(uow, pk)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", status_code=201, response_model=PostSingle)
async def create_post(
        uow: UOWDep,
        post: PostCreate,
        user: User = Depends(current_active_user)
):
    post = await PostsService().add_post(uow, post)
    return post
