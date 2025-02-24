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
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_one(
            self,
            item_id: int,
    ) -> Base | None:
        return await self.session.get(self.model, item_id)

    async def add_one(
            self,
            data: BaseModel,
    ) -> Base:
        item = self.model(**data.model_dump())
        self.session.add(item)
        await self.session.commit()
        return item
