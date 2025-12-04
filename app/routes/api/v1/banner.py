import logging
from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.models.article import Article
from app.models.user import User
from app.models.banner_image import BannerImage
from typing import List, Optional
import os
from app.core.jwt import verify_token
from app.services.file_service import FileService
from app.schemas.banner_image import BannerImageResponse
from app.dependencies.auth import get_db, get_current_user_id, get_current_user
from app.repositories.banner_repository import BannerRepository
from app.services.banner_service import BannerService

log = logging.getLogger("uvicorn.error")
router = APIRouter(prefix="/v1/banners", tags=["banners"])

@router.get("", response_model=List[BannerImageResponse])
def get_all_banners(db: Session = Depends(get_db)):
    return db.query(BannerImage).all()

# GET banner by id
# @router.get("/{banner_id}", response_model=BannerImageResponse)
@router.get("/{banner_id}")
def get_article(
    banner_id: int,
    db: Session = Depends(get_db),
):
    banner = db.query(BannerImage).filter(BannerImage.id == banner_id).first()
    if not banner or banner is None:
        raise HTTPException(status_code=404, detail="Banner Image not found")
    
    log.info(f"🗑 Found banner file: {banner.file_path}")
    return banner

@router.post("")
async def add_banner(
    banner_id: int,
    banner: UploadFile,
    current_user: User = Depends(get_current_user),
    article_id: int = Form(None),
    db: Session = Depends(get_db)
):
    try:
        updatedBanner = await BannerService.update_banner(db, banner_id, banner, current_user.id, article_id )
        return updatedBanner
    except Exception as e:
        log.error("❌ Error while updating banner", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update banner: {str(e)}")
    
@router.put("/{banner_id}")
async def update_banner(
    banner_id: int,
    banner: UploadFile,
    current_user: User = Depends(get_current_user),
    article_id: int = Form(None),
    db: Session = Depends(get_db)
):
    
    try:
        log.info(f"Current User: {current_user.id}")
        updatedBanner = await BannerService.update_banner(db, banner_id, banner, current_user.id, article_id )
        return updatedBanner
    except Exception as e:
        log.error("❌ Error while updating banner", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update banner: {str(e)}")
   

@router.delete("/{banner_id}")
async def delete_banner(
    banner_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    # 1️⃣ Find banner
    banner = db.query(BannerImage).filter(BannerImage.id == banner_id).first()

    if not banner or banner is None:
        raise ValueError("Banner not found")
    
    # 2️⃣ Ensure the current user owns the article
    article = db.query(Article).filter(Article.id == banner.article_id).first()

    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Unauthorized: Not your article")
    
    # 3️⃣ Delete banner file
    log.info(f"🗑 Deleting banner file: {banner.file_path}")
    await FileService.deleteFile(banner.file_path)

    db.delete(banner)
    db.commit()

    return {"message": "Banner deleted successfully"}
