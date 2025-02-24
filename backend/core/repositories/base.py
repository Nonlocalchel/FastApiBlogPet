from abc import ABC, abstractmethod
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Base


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one():
        raise NotImplementedError

    @abstractmethod
    async def get_one():
        raise NotImplementedError

    @abstractmethod
    async def get_all():
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
            self,
    ) -> Sequence[Base]:
        stmt = select(self.model).order_by(self.model.id)
        res = await self.session.execute(stmt) # не self.session.scallars потому что scalars делал линивую загрузку. Это работало в случае, когда сессия была открытой до следующего запроса
        res = [row[0].transform_model_to_dict() for row in res.all()]
        return res

    async def get_one(self, **filter_by):
        stmt = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        try:
            res = res.scalar_one().transform_model_to_dict()
            return res
        except Exception:
            return None


    async def add_one(
            self,
            data: BaseModel,
    ) -> Base:
        item = self.model(**data.model_dump())
        self.session.add(item)
        await self.session.commit()
        return item
