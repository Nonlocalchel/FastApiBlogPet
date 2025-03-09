from core.schemas.post import PostCreate, PostEdit
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

    async def get_post_by_id(self, uow: IUnitOfWork, post_id: int):
        async with uow:
            posts = await uow.posts.get_one(id=post_id)
            return posts

    async def edit_task(self, uow: IUnitOfWork, task_id: int, task: PostEdit):
        tasks_dict = task.model_dump()
        async with uow:
            post = await uow.tasks.edit_one(task_id, tasks_dict)
            await uow.commit()
            return post['id']