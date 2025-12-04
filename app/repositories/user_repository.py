from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    @staticmethod
    def find_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    @staticmethod
    def find_by_id(db: Session, id: int):
        return db.query(User).filter(User.id == id).first()
    @staticmethod
    def find_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()
    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()
    def create(self, user: User):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    # @staticmethod
    # def create(db: Session, data):
    #     hashed = bcrypt.hash(data.password)
    #     new_user = User(
    #         username=data.username,
    #         email=data.email,
    #         name=data.name,
    #         password=hashed
    #     )
    #     db.add(new_user)
    #     db.commit()
    #     db.refresh(new_user)
    #     return new_user
    @staticmethod
    def find_all(self):
        return self.query(User).all()
    @staticmethod
    def update(db: Session, user: User, data):
        if data.username:
            user.username = data.username
        if data.email:
            user.email = data.email
        if data.name:
            user.name = data.name

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete(db: Session, user: User):
        db.delete(user)
        db.commit()