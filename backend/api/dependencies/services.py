from typing import Annotated

from fastapi import Depends

from repositories import PostsRepository
from services import PostsService


def posts_service():
    return PostsService(PostsRepository)


PostsServiceDep = Annotated[PostsService, Depends(posts_service)]
