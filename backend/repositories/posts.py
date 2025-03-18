from core.models import Post
from repositories.base import SQLAlchemyRepository


class PostsRepository(SQLAlchemyRepository):
    model = Post