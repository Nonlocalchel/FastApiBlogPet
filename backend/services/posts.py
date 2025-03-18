from repositories import AbstractRepository
from core.schemas.posts import PostCreate, PostEdit


class PostsService:
    def __init__(self, users_repo: AbstractRepository):
        self.posts_repo: AbstractRepository = users_repo()

    async def get_posts(self):
        posts = await self.posts_repo.get_all()
        return posts

    async def get_post_by_id(self, post_id: int):
        posts = await self.posts_repo.get_one(id=post_id)
        return posts

    async def add_post(self, post: PostCreate):
        posts_dict = post.model_dump()
        post_id = await self.posts_repo.add_one(posts_dict)
        return post_id

    async def update_post(self,post_id: int, post: PostEdit):
        posts_dict = post.model_dump()
        post = await self.posts_repo.edit_one(post_id, posts_dict)
        return post

    async def delete_post(self, post_id: int):
        is_delete = await self.posts_repo.delete_one(post_id)
        return is_delete
