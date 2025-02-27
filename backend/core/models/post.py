from sqlalchemy import String, ForeignKey, DateTime, sql, Column
from sqlalchemy.orm import relationship, Mapped, mapped_column

from core.models import Base


class Post(Base):
    title: Mapped[str] = mapped_column(String(100), unique=False)
    date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=sql.func.now())
    body: Mapped[str] = mapped_column(
        String(350),
        default="",
        server_default="",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )

    user: Mapped["User"] = relationship("User", back_populates="posts")

