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

def get_current_user(Authorization: str = Header(...), db: Session = Depends(get_db)):

    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = Authorization.split(" ")[1]

    try:
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        user_id = int(payload["sub"])
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")

        user = UserRepository.find_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user

    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


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
