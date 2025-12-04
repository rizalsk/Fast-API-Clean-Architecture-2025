from app.models.banner_image import BannerImage
from sqlalchemy.orm import Session

class BannerRepository:
    # def __init__(self, db):
    #     self.db = db

    @staticmethod
    def create(db: Session, banner: BannerImage):
        db.add(banner)
        db.commit()
        db.refresh(banner)
        return banner
    
    @staticmethod
    def get_by_article(db: Session, article_id: int):
        return db.query(BannerImage).filter(BannerImage.article_id == article_id).all()
    
    @staticmethod
    def find_banner_by_id(db: Session, banner_id: int):
        return db.query(BannerImage).filter(BannerImage.id == banner_id).first()