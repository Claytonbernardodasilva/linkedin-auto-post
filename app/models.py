# app/models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base # type: ignore

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    post_date = Column(DateTime(timezone=True), server_default=func.now())
    linkedin_post_id = Column(String(100))
    status = Column(String(20), default="PENDING")
    interactions = relationship("Interaction", back_populates="post")

class Interaction(Base):
    __tablename__ = "interactions"
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_name = Column(String(255))
    comment = Column(Text)
    likes_count = Column(Integer, default=0)
    comment_date = Column(DateTime(timezone=True), server_default=func.now())

    post = relationship("Post", back_populates="interactions")
