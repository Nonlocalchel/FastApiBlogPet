from core.models import User
from core.repositories.base import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User
