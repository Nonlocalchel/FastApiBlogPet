from core.schemas.post import PostCreate, PostEdit
from core.utils.unit_of_work import IUnitOfWork


class PostsService:

    async def get_posts(self, uow: IUnitOfWork):
        async with uow:
            posts = await uow.posts.get_all()
            return posts

    async def get_post_by_id(self, uow: IUnitOfWork, post_id: int):
        async with uow:
            posts = await uow.posts.get_one(id=post_id)
            return posts

    async def add_post(self, uow: IUnitOfWork, post: PostCreate):
        posts_dict = post.model_dump()
        async with uow:
            post_id = await uow.posts.add_one(posts_dict)
            await uow.commit()
            return post_id

    async def update_post(self, uow: IUnitOfWork, post_id: int, post: PostEdit):
        posts_dict = post.model_dump()
        async with uow:
            post = await uow.posts.edit_one(post_id, posts_dict)
            await uow.commit()
            return post

    async def delete_post(self, uow: IUnitOfWork, post_id: int):
        async with uow:
            is_delete = await uow.posts.delete_one(post_id)
            return is_delete
