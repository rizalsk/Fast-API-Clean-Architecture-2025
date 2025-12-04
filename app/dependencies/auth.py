from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.core.jwt import verify_token
from app.repositories.user_repository import UserRepository

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    Authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Extract user from JWT Authorization header.
    """
    if not Authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")

    token = Authorization.split(" ")[1]

    try:
        payload = verify_token(token)
        user_id = int(payload["sub"])

        user = UserRepository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(401, "User not found")

        return user

    except Exception:
        raise HTTPException(401, "Invalid or expired token")


def get_current_user_id(
    Authorization: str = Header(...),
):
    if not Authorization.startswith("Bearer "):
        raise HTTPException(401, "Invalid authorization header")

    token = Authorization.split(" ")[1]

    try:
        payload = verify_token(token)
        return int(payload["sub"])
    except Exception:
        raise HTTPException(401, "Invalid or expired token")
