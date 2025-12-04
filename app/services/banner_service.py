from app.models.banner_image import BannerImage
from typing import Optional
from fastapi import File, UploadFile, HTTPException
from app.services.file_service import FileService
from app.repositories.banner_repository import BannerRepository

class BannerService:
    @staticmethod
    async def add_banner(db, file: Optional[UploadFile] = File(None), user_id: int = None, article_id: int = None):
        uploadedBanner = await FileService.doUpload(file)
        filename, file_path = uploadedBanner['filename'], uploadedBanner['file_path']
        banner = BannerImage(
            file_path=file_path,
            filename=filename,
            created_by=user_id,
            article_id=article_id
        )
        db.add(banner)
        db.commit()
        db.refresh(banner)
        return banner
    
    async def update_banner(db, banner_id: int, file: Optional[UploadFile] = File(None), user_id: int = None, article_id: int = None):
        # 1. upload new banner
        # 2. update table banner
        # 3. remove old banner
        # 4. return new banner

        if not file or file is None:
            raise HTTPException(status_code=400, detail="No input file")
    
        current_banner = BannerRepository.find_banner_by_id(banner_id=banner_id, db=db)

        if current_banner is None:
            raise HTTPException(status_code=400, detail="Banner not found")
        
        uploadedBanner = await FileService.doUpload(file)
        updatedfilename, updatedfilepath = uploadedBanner["filename"], uploadedBanner["file_path"]

        await FileService.deleteFile(current_banner.file_path)

        if updatedfilename and updatedfilepath:
            current_banner.file_path = updatedfilepath
            current_banner.filename = updatedfilename
        if user_id:
            current_banner.created_by = user_id
        if article_id:
            current_banner.article_id = article_id

        db.commit()
        db.refresh(current_banner)

        return current_banner
    
