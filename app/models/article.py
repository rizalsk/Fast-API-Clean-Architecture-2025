from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Article(Base):
    __tablename__ = "articles"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    cover_image = Column(String(255), nullable=True)
    title = Column(String(255))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    banners = relationship(
        "app.models.banner_image.BannerImage",  # fully-qualified string
        back_populates="article",
        cascade="all, delete-orphan"
    )
