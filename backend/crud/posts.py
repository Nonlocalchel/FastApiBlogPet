from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.post import Post
from core.schemas.post import PostCreate


async def get_post_list(
        session: AsyncSession,
) -> Sequence[Post]:
    stmt = select(Post).order_by(Post.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_post(
        session: AsyncSession,
        post_id: int,
) -> Post | None:
    return await session.get(Post, post_id)


async def create_post(
        session: AsyncSession,
        post_create: PostCreate,
) -> Post:
    post = Post(**post_create.model_dump())
    session.add(post)
    await session.commit()
    # await session.refresh(post)
    return post
