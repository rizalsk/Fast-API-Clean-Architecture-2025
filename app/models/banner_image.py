from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class BannerImage(Base):
    __tablename__ = "banner_images"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True)
    file_path = Column(String(255))
    filename = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer)
    article_id = Column(Integer, ForeignKey("articles.id"))

    article = relationship(
        "app.models.article.Article",  # fully-qualified string
        back_populates="banners"
    )
