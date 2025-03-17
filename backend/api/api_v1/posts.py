from typing import List

from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.api_v1.authentication.fastapi_users import current_active_user
from api.dependencies.services import PostsServiceDep
from core.config import settings
from core.models import User
from core.schemas.post import PostList, PostCreate, PostSingle, PostEdit

router = APIRouter(
    prefix=settings.api.v1.posts,
    tags=["Posts"],
)


@router.get("/", response_model=List[PostList])
async def get_posts(
        posts_service: PostsServiceDep,
):
    posts = await posts_service.get_posts()
    return posts


@router.get("/{pk}", response_model=PostSingle)
async def post_single(
        posts_service: PostsServiceDep,
        pk: int
):
    post = await posts_service.get_post_by_id(pk)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", status_code=201)
async def create_post(
        posts_service: PostsServiceDep,
        post: PostCreate,
        user: User = Depends(current_active_user),
):
    post = await posts_service.add_post(post)
    return post


@router.patch("/{pk}")
async def update_product(
        posts_service: PostsServiceDep,
        post: PostEdit,
        pk: int,
        user: User = Depends(current_active_user)
):
    post = await posts_service.update_post(pk, post)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{pk}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        posts_service: PostsServiceDep,
        pk: int,
        user: User = Depends(current_active_user)
) -> None:
    post = await posts_service.delete_post(pk)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post
