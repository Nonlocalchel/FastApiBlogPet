from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from core.schemas.user import UserRead


class PostBase(BaseModel):
    title: str = ''
    text: str = ''


class PostList(PostBase):
    id: Optional[int]
    date: Optional[datetime]
    user: UserRead | None


class PostSingle(PostList):
    pass

class PostCreate(PostBase):

    class Config:
        from_attributes = True
