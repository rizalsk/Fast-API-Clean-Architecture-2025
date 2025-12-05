from fastapi import APIRouter, Depends, HTTPException, Header, Form, UploadFile, File
from sqlalchemy.orm import Session
from fastapi import status
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.database.session import SessionLocal
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.schemas.auth import LoginSchema, TokenSchema, TokenRefreshRequest, TokenRefreshResponse, LoginTokenSchema
from app.core.jwt import verify_token
from app.core.config import settings
from app.repositories.user_repository import UserRepository
from app.dependencies.logger import log
from app.dependencies.auth import get_db, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

ACCESS_EXPIRES = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
REFRESH_EXPIRES = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(user.username, user.email, user.password)

@router.post("/login", response_model=LoginTokenSchema)
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    try:
        tokens = AuthService.login(db, payload.email, payload.password)
        user = UserRepository.find_by_email(db, payload.email)
        if not tokens:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access, refresh, test = tokens
        return LoginTokenSchema(
            access_token=access,
            refresh_token=refresh,
            expires_in=ACCESS_EXPIRES,
            refresh_expires_in=REFRESH_EXPIRES,
            user=UserResponse.model_validate(user)
        )
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/refresh", response_model=TokenRefreshResponse)
def refresh_token(data: TokenRefreshRequest):
    try:
        new_tokens = AuthService.refresh_access_token(data.refresh_token)
        return new_tokens
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UserResponse)
def get_me(
    db: Session = Depends(get_db),
    authorization: str = Header(None)
):

    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing authorization header")

    token = authorization.split(" ")[1]

    user = AuthService.get_current_user(db, token)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    username: str = Form(None),
    email: str = Form(None),
    name: str = Form(None),
    password: str = Form(None),
    password_confirmation: str = Form(None),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user),
):
    try:
        data = UserUpdate(username=username, email=email, name=name)

        updated_user = await UserService.update_profile(
            db=db,
            user_id=current_user.id,
            data=data,
            avatar=avatar,
            password=password,
            password_confirmation=password_confirmation,
        )
        return updated_user
    except Exception as e:
        log.error("❌ Error while updating profile", exc_info=True)
        raise HTTPException(status_code=500, detail=f"{str(e)}")