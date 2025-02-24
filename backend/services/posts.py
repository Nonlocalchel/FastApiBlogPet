from core.schemas.post import PostCreate
from core.utils.unit_of_work import IUnitOfWork


class PostsService:
    async def add_post(self, uow: IUnitOfWork, post: PostCreate):
        async with uow:
            post_id = await uow.posts.add_one(post)
            await uow.commit()
            return post_id

    async def get_posts(self, uow: IUnitOfWork):
        async with uow:
            posts = await uow.posts.get_all()
            return posts

    async def get_post(self, uow: IUnitOfWork, post_id: int):
        async with uow:
            posts = await uow.posts.get_one()
            return posts