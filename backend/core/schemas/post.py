from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from core.models import User
from core.schemas.user import UserRead


class PostBase(BaseModel):
    title: str = ''
    text: str = ''


class PostList(PostBase):
    id: Optional[int]
    date: Optional[datetime]
    user: UserRead | None
    parent_id: Optional[int] = None


class PostSingle(PostList):
    pass

class PostCreate(PostBase):
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True
