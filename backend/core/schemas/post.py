from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from core.schemas.user import UserRead


class PostBase(BaseModel):
    title: str = ''
    text: str = ''


class PostList(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int]
    date: Optional[datetime]
    user: UserRead | None
    # user: Optional[UserRead]| None

    # class Config:
    #     from_attributes = True




class PostSingle(PostList):
    pass

class PostCreate(PostBase):

    class Config:
        from_attributes = True
