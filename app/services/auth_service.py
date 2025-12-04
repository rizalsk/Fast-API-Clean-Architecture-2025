from fastapi import UploadFile
import logging
from app.core.security import verify_password
from app.core.jwt import create_access_token, create_refresh_token
from app.repositories.user_repository import UserRepository
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.jwt import decode_access_token, verify_token
from app.core.security import hash_password
import os
import uuid

UPLOAD_DIR = "app/assets/uploads"

log = logging.getLogger("uvicorn.error")

class AuthService:
    # def __init__(self, db: Session):
    #     self.user_repo = UserRepository(db)

    @staticmethod
    async def register(db: Session, username: str, email: str, password: str, name: str, avatar: UploadFile = None):
        hashed = hash_password(password)
        user = User(username=username, email=email, name=name, password=hashed)
        if avatar is not None:
            filename = f"{uuid.uuid4()}_{avatar.filename}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            # Save file to disk
            with open(file_path, "wb") as f:
                f.write(await avatar.read())
            user.avatar = file_path
        return UserRepository.create(db, user)

    @staticmethod
    def login(db, email: str, password: str):
        user = UserRepository.find_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.password):
            return None
        
        access = create_access_token({"sub": str(user.id)})
        refresh = create_refresh_token({"sub": str(user.id)})

        return access, refresh, user

    @staticmethod
    def get_current_user(db, token: str):
        payload = decode_access_token(token)
        if not payload:
            return None

        user_id = payload.get("sub")
        if not user_id:
            return None

        return UserRepository.find_by_id(db, user_id)
    
    @staticmethod
    def refresh_access_token(refresh_token: str):
        payload = verify_token(refresh_token)
        if not payload:
            raise ValueError("Invalid or expired refresh token")

        user_id = int(payload["sub"])
        if not user_id:
            raise ValueError("Invalid token payload")

        new_access_token = create_access_token({"sub": str(user_id)})
        return {"access_token": new_access_token}