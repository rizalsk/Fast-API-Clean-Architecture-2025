from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from app.schemas.banner_image import BannerImageResponse

class BannerImageSchema(BaseModel):
    id: int
    file_path: str
    filename: str
    class Config:
        orm_mode = True

class ArticleCreate(BaseModel):
    title: str
    content: str

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime
    cover_image: Optional[str] = None
    banners: List[BannerImageSchema] = []

    class Config:
        orm_mode = True
