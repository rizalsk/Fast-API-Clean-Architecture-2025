from app.models.article import Article
from sqlalchemy.orm import Session

class ArticleRepository:
    def __init__(self, db):
        self.db = db
    @staticmethod
    def create(db: Session, article: Article):
        db.add(article)
        db.commit()
        db.refresh(article)
        return article

    @staticmethod
    def find_all(db: Session):
        return db.query(Article).all()

    @staticmethod
    def find_by_id(db: Session, id: int):
        return db.query(Article).filter(Article.id == id).first()

    @staticmethod
    def delete(self, article):
        self.db.delete(article)
        self.db.commit()
