from core.models import User
from repositories.base import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User
