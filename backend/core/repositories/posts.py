from core.models import Post
from core.repositories.base import SQLAlchemyRepository


class PostsRepository(SQLAlchemyRepository):
    model = Post