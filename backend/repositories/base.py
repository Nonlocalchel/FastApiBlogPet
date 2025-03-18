from abc import ABC, abstractmethod

from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import selectinload

from core.models import Base
from core.utils.db_session import session_factory


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, *args, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def get_all(self):
        async with session_factory() as session:
            stmt = select(self.model).options(selectinload(self.model.user)).order_by(self.model.id)
            res = await session.execute(stmt)
            res = [row[0].transform_model_to_dict() for row in res.all()]
            return res

    async def get_one(self, **filter_by):
        async with session_factory() as session:
            stmt = select(self.model).filter_by(**filter_by)
            res = await session.execute(stmt)
            try:
                res = res.scalar_one().transform_model_to_dict()
                return res
            except Exception:
                return None

    async def add_one(
            self,
            data: dict,
    ) -> Base:
        async with session_factory() as session:
            stmt = insert(self.model).values(**data).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def edit_one(self, post_id: int, data: dict) -> int:
        async with session_factory() as session:
            stmt = update(self.model).values(**data).filter_by(id=post_id).returning(self.model)
            res = await session.execute(stmt)
            await session.commit()
            row = res.first()
            return row[0] if row is not None else None


    async def delete_one(
            self,
            post_id: int,
    ) -> bool | None:
        async with session_factory() as session:
            stmt = delete(self.model).where(self.model.id == post_id)
            res = await session.execute(stmt)
            await session.commit()
            return None if res.rowcount == 0 else True
