from repositories.user_repository import UserRepository
from fastapi import HTTPException, UploadFile
from app.schemas.user import UserUpdate
from app.models.user import User
from app.services.file_service import FileService
from typing import Optional

class UserService:

    @staticmethod
    def get_users(db):
        return UserRepository.find_all(db)

    @staticmethod
    def get_user(db, user_id):
        user = UserRepository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def create_user(db, data):
        existing = UserRepository.find_by_username(db, data.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already exists")

        return UserRepository.create(db, data)

    @staticmethod
    def update_user(db, user_id, data):
        user = UserRepository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return UserRepository.update(db, user, data)

    @staticmethod
    def delete_user(db, user_id):
        user = UserRepository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        UserRepository.delete(db, user)
        return True
    
    @staticmethod
    async def update_profile(
        db,
        user_id: int,
        data: UserUpdate,
        avatar: Optional[UploadFile] = None,
        password: str = None,
        password_confirmation: str = None,
    ):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ValueError("User not found")

        if data.username is not None:
            user.username = data.username
        if data.email is not None:
            user.email = data.email
        if data.name is not None:
            user.name = data.name

        if password is not None:
            if password_confirmation != password:
                raise ValueError("Password confirmation miss match!")


        if avatar is not None:
            if user.avatar:
                FileService.delete(user.avatar)

            uploaded = await FileService.doUpload(avatar)
            user.avatar = uploaded["file_path"]

        db.commit()
        db.refresh(user)
        return user