from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, sql
from sqlalchemy.orm import relationship

from core.models import Base


class Post(Base):
    __tablename__ = "microblog_posts"

    title = Column(String)
    text = Column(String(350))
    date = Column(DateTime(timezone=True), server_default=sql.func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")



posts = Post.__table__
