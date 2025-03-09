from abc import ABC, abstractmethod
from typing import Sequence

from pydantic import BaseModel
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Base
from core.schemas.post import PostList


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

    async def get_all(self):
        stmt = select(self.model).options(selectinload(self.model.user)).order_by(self.model.id)
        res = await self.session.execute(stmt)
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

    async def edit_one(self, post_id: int, data: dict) -> int:
        stmt = update(self.model).values(**data).filter_by(id=post_id).returning(self.model.id)
        res = await self.session.execute(stmt)
        return res.scalar_one()
