import os
import logging
from fastapi import UploadFile, File
from app.repositories.article_repository import ArticleRepository
from app.repositories.banner_repository import BannerRepository
from app.core.config import settings
from app.models.article import Article
from app.models.banner_image import BannerImage
import os
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.services.file_service import FileService

UPLOAD_DIR = "app/assets/uploads"

log = logging.getLogger("uvicorn.error")

class ArticleService:
    # def __init__(self, db):
    #     self.db = db
    #     self.article_repo = ArticleRepository(db)
    #     self.banner_repo = BannerRepository(db)

    @staticmethod
    async def create_article(db, author_id, title, content, cover_image, banners):
        log.info("🛠 Creating article in database...")

        article = Article(author_id=author_id, title=title, content=content)
        if cover_image is not None:
            uploaded = await FileService.doUpload(cover_image)
            file_path = uploaded["file_path"]
            article.cover_image = file_path

        db.add(article)
        db.commit()
        db.refresh(article)

        log.info(f"📝 Article saved: ID {article.id}")

        if banners:
            for idx, file in enumerate(banners):
                try:
                    uploadedBanner = await FileService.doUpload(file)
                    filenameB, file_pathB = uploadedBanner["filename"], uploadedBanner["file_path"]
                    banner_record = BannerImage(
                        file_path=file_pathB,
                        filename=filenameB,
                        created_by=author_id,
                        article_id=article.id
                    )
                    db.add(banner_record)
                    log.info(f"🗄 DB record created for banner[{idx}]")

                except Exception:
                    log.error(f"❌ Failed to process banner[{idx}]", exc_info=True)

            db.commit()
            log.info("📦 All banners processed and committed")

        return article
    
    
    @staticmethod
    async def update_article(
        db,
        article_id: int,
        author_id: int,
        title: str = None,
        content: str = None,
        image_cover: Optional[UploadFile] = File(None),
        banners: Optional[List[UploadFile]] = None,
        remove_banner_ids: Optional[List[int]] = None,
    ):
        """
        Update article:
        - Update title/content
        - Add new banners (optional)
        - Remove old banners by ID (optional)
        """

        # Fetch article
        article = db.query(Article).filter(Article.id == article_id).first()
        if not article:
            raise ValueError("Article not found")

        # Check ownership
        if article.author_id != author_id:
            raise PermissionError("You do not own this article")

        log.info(f"🛠 Updating Article {article_id}")

        # Update basic fields
        if title is not None:
            article.title = title
        if content is not None:
            article.content = content
        if image_cover is not None:
            log.info(f"🗑 service filedelete: {article.cover_image}")
            await FileService.deleteFile(article.cover_image)
            uploaded = await FileService.doUpload(image_cover)
            file_path = uploaded["file_path"]
            article.image_cover = file_path

        # ---------------------------------------------
        # 🔥 STEP 1 — Remove old banners
        # ---------------------------------------------
        log.info(f"🗑 remove_banner_ids: {remove_banner_ids}")
        if remove_banner_ids:

            for banner_id in remove_banner_ids:
                banner = (
                    db.query(BannerImage)
                    .filter(BannerImage.id == banner_id,
                            BannerImage.article_id == article_id)
                    .first()
                )
                if not banner:
                    log.warning(f"⚠ Banner ID {banner_id} not found or not part of article")
                    continue

                if os.path.exists(banner.file_path):
                    await FileService.deleteFile(banner.file_path)

                # Remove DB record
                db.delete(banner)
                log.info(f"🗄 Removed banner record id={banner_id}")

        # ---------------------------------------------
        # 🔥 STEP 2 — Add new banners
        # ---------------------------------------------
        if banners:
            for idx, file in enumerate(banners):
                try:
                    uploaded = await FileService.doUpload(file)
                    file_path = uploaded["file_path"]
                    filename = uploaded["filename"]

                    # Save DB record
                    banner_record = BannerImage(
                        file_path=file_path,
                        filename=filename,
                        created_by=author_id,
                        article_id=article.id
                    )
                    db.add(banner_record)
                    log.info(f"🗄 DB record created for new banner[{idx}]")

                except Exception:
                    log.error(f"❌ Failed to process new banner[{idx}]", exc_info=True)

        db.commit()
        db.refresh(article)

        log.info(f"✔ Article {article_id} updated successfully")

        # ----------------------------
        # Load banners for response
        # ----------------------------
        article_banners = db.query(BannerImage).filter(BannerImage.article_id == article.id).all()
        article.banners = article_banners  # dynamic attribute for serialization

        return article

    @staticmethod
    def delete_article(db: Session, article_id: int, author_id: int):
        """
        Delete an article and its associated banners
        """

        log.info(f"🗑 Attempting to delete article ID={article_id}")

        article = db.query(Article).filter(Article.id == article_id).first()

        if not article:
            raise ValueError("Article not found")

        # Authorization check
        if article.author_id != author_id:
            raise PermissionError("You do not own this article")

        # -------------------------------------------------
        # 🔥 DELETE BANNERS FIRST
        # -------------------------------------------------

        banners = db.query(BannerImage).filter(BannerImage.article_id == article_id).all()

        log.info(f"🗑 Deleting {len(banners)} banners for Article ID={article_id}")

        for banner in banners:
            # Delete file
            if banner.file_path and os.path.exists(banner.file_path):
                try:
                    os.remove(banner.file_path)
                    log.info(f"🗑 Deleted file: {banner.file_path}")
                except Exception:
                    log.error(f"❌ Failed to delete file: {banner.file_path}", exc_info=True)

            # Delete DB record
            db.delete(banner)
            log.info(f"🗄 Deleted banner DB record ID={banner.id}")

        # -------------------------------------------------
        # 🔥 DELETE ARTICLE
        # -------------------------------------------------

        db.delete(article)
        db.commit()

        log.info(f"✔ Article ID={article_id} deleted successfully")

        return {"message": "Article deleted successfully"}