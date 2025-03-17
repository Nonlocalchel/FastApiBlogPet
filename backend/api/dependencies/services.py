from typing import Annotated

from fastapi import Depends

from core.repositories.posts import PostsRepository
from services.posts import PostsService


def posts_service():
    return PostsService(PostsRepository)


PostsServiceDep = Annotated[PostsService, Depends(posts_service)]
