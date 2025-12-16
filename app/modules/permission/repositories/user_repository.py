# app/repositories/user_repository.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.modules.permission.models.role import Role

class UserRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(User).all()

    @staticmethod
    def find_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def find_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create(db: Session, user: User, role_ids: list[int] = []):
        if role_ids:
            roles = db.query(Role).filter(Role.id.in_(role_ids)).all()
            user.roles = roles
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: User):
        db.delete(user)
        db.commit()
