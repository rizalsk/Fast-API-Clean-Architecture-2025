from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.modules.permission.schemas.user_schema import UserResponse
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password
from typing import List
from app.modules.permission.middleware.permission_middleware import has_access
from app.modules.permission.services.user_service import UserService


router = APIRouter(
    prefix="/api/v1/guarded/users",
    tags=["Users"]
)

# -----------------------------------------------------
# GET /users
# Required Permission: Manage User:view
# -----------------------------------------------------
@router.get(
    "/", 
    response_model=List[UserResponse],
    dependencies=[Depends(has_access("Manage User:view"))],
)
def list_users(db: Session = Depends(get_db), ):
    users = UserService.list_users(db)
    return users


# -----------------------------------------------------
# POST /users
# Required Permission: Manage User:create
# -----------------------------------------------------
@router.post(
    "/", 
    response_model=UserResponse,
    dependencies=[Depends(has_access("Manage User:create"))]
)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):

    exists = db.query(User).filter(User.email == payload.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        username=payload.username,
        email=payload.email,
        name=payload.name,
        avatar=payload.avatar,
        password=hash_password(payload.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -----------------------------------------------------
# GET /users/{id}
# Required Permission: Manage User:view
# -----------------------------------------------------
@router.get("/{user_id}", response_model=UserResponse,
            dependencies=[Depends(has_access("Manage User:view"))])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -----------------------------------------------------
# PUT /users/{id}
# Required Permission: Manage User:edit
# -----------------------------------------------------
@router.put("/{user_id}", response_model=UserResponse,
            dependencies=[Depends(has_access("Manage User:edit"))])
def update_user(
    user_id: int,
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = payload.username
    user.email = payload.email
    user.name = payload.name
    user.avatar = payload.avatar
    user.password = hash_password(payload.password)

    db.commit()
    db.refresh(user)

    return user


# -----------------------------------------------------
# DELETE /users/{id}
# Required Permission: Manage User:delete
# -----------------------------------------------------
@router.delete("/{user_id}", dependencies=[Depends(has_access("Manage User:delete"))])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


# Apply middleware this router
# router.dependencies.append(Depends(PermissionRequired("Manage Article:create")))
