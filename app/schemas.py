# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class InteractionBase(BaseModel):
    author_name: str
    comment: Optional[str]
    likes_count: int

class InteractionCreate(InteractionBase):
    pass

class Interaction(InteractionBase):
    id: int
    comment_date: datetime

class Config:
    from_attributes = True

class PostBase(BaseModel):
    content: str

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    post_date: datetime
    linkedin_post_id: Optional[str]
    status: str
    interactions: List[Interaction] = []

    class Config:
        orm_mode = True
