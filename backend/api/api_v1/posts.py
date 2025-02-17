from typing import List, Annotated


from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.auth.fastapi_users import current_active_user, current_active_superuser
from core.config import settings
from core.models import db_helper, User
from core.schemas.post import PostList, PostCreate, PostSingle
from crud import posts as posts_services

# http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.posts,
    tags=["Posts"],
    # dependencies=[Depends(http_bearer)],
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
        post_create: PostCreate,
        user: User = Depends(current_active_user)
):
    user = await posts_services.create_post(
        session=session,
        post_create=post_create,
    )
    return user
