from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped


class IntIdPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
