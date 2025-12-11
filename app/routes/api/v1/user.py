from fastapi import APIRouter, Depends
from database.session import SessionLocal
from services.user_service import UserService
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from typing import List
from core.jwt import verify_token
from app.dependencies.auth import get_db, get_current_user

router = APIRouter(
    prefix="/v1/users", 
    tags=["Users"],
    dependencies=[Depends(get_current_user)]  #like router-level middleware
)

@router.post("/", response_model=UserResponse)
def create_user(payload: UserCreate, db=Depends(get_db)):
    return UserService.create_user(db, payload)

@router.get("/", response_model=List[UserResponse])
def list_users(db=Depends(get_db)):
    return UserService.get_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db=Depends(get_db)):
    return UserService.get_user(db, user_id)

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, payload: UserUpdate, db=Depends(get_db)):
    return UserService.update_user(db, user_id, payload)

@router.delete("/{user_id}")
def delete_user(user_id: int, db=Depends(get_db)):
    UserService.delete_user(db, user_id)
    return {"message": "User deleted"}
