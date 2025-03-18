from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from core.schemas.users import UserRead


class PostBase(BaseModel):
    title: str = ''
    body: str = ''


class PostList(PostBase):
    id: Optional[int]
    date: Optional[datetime]
    user_id: int | None


class PostSingle(PostList):
    pass


class PostEdit(PostBase):
    pass


class PostCreate(PostBase):
    model_config = ConfigDict(from_attributes=True)
