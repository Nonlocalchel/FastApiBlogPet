from sqlalchemy import Column, String, Integer, sql, ForeignKey, DateTime, sql
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin


class Post(Base, IntIdPkMixin):
    __tablename__ = "microblog_posts"

    # id = Column(Integer, primary_key=True, index=True, unique=True)
    title = Column(String)
    text = Column(String(350))
    date = Column(DateTime(timezone=True), server_default=sql.func.now())
    # user = Column(String, ForeignKey('users.id'))
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user_id = relationship("User")
