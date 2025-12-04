from fastapi import APIRouter, Depends
from database.session import SessionLocal
from services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from typing import List
from core.jwt import verify_token

router = APIRouter(prefix="/v1/users", tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str):
    data = verify_token(token)
    return data["sub"]


# CREATE (Public Registration)
@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate, db=Depends(get_db)):
    return UserService.create_user(db, payload)


# READ ALL
@router.get("/", response_model=List[UserResponse])
def list_users(token: str, db=Depends(get_db)):
    get_current_user(token)
    return UserService.get_users(db)


# READ ONE
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, token: str, db=Depends(get_db)):
    get_current_user(token)
    return UserService.get_user(db, user_id)


# UPDATE
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, token: str, db=Depends(get_db)):
    get_current_user(token)
    return UserService.update_user(db, user_id, payload)


# DELETE
@router.delete("/{user_id}")
def delete_user(user_id: int, token: str, db=Depends(get_db)):
    get_current_user(token)
    UserService.delete_user(db, user_id)
    return {"message": "User deleted"}
