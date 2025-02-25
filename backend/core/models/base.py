from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy.orm import declared_attr

from core.config import settings
from utils import camel_case_to_snake_case


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"

    def transform_model_to_dict(self):
        # Обработка простых колонок
        data = {column.name: getattr(self, column.name) for column in self.__table__.columns}

        # Обработка отношений (вложенных моделей)
        for relation in self.__mapper__.relationships:
            related_obj = getattr(self, relation.key)
            if related_obj is None:
                data[relation.key] = None
            # Если связь возвращает список объектов (one-to-many, many-to-many)
            elif isinstance(related_obj, list):
                data[relation.key] = [
                    item.transform_model_to_dict() if isinstance(item, Base) else item
                    for item in related_obj
                ]
            # Если связь возвращает один объект (one-to-one, many-to-one)
            else:
                data[relation.key] = (
                    related_obj.transform_model_to_dict()
                    if isinstance(related_obj, Base)
                    else related_obj
                )
        return data
