from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from ..types.user_id import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    pass

    @classmethod
    def get_db(cls, session: "AsyncSession") -> SQLAlchemyUserDatabase:
        return SQLAlchemyUserDatabase(session, User)
