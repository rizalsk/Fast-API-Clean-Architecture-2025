import logging
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, Header
from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from app.services.article_service import ArticleService
from app.models.article import Article
from app.models.user import User
from app.schemas.article import ArticleResponse
from typing import List
import os
from app.core.jwt import verify_token, decode_access_token
from app.repositories.user_repository import UserRepository

log = logging.getLogger("uvicorn.error")
router = APIRouter(prefix="/v1/articles", tags=["articles"])

UPLOAD_DIR = "app/assets/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(Authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    Extract JWT from Authorization header.
    Expected format: 'Bearer <token>'
    """
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

def get_current_user_id(Authorization: str = Header(...)):
    """
    Extract JWT from Authorization header.
    Expected format: 'Bearer <token>'
    """
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = Authorization.split(" ")[1]

    try:
        decoded = verify_token(token)
        return int(decoded["sub"])
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.get("", response_model=List[ArticleResponse])
def get_all_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

@router.get("/me", response_model=List[ArticleResponse])
def get_my_articles(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    articles = db.query(Article).filter(Article.author_id == current_user_id).all()
    return articles

@router.get("/me/{article_id}", response_model=ArticleResponse)
def get_my_article_by_id(
    article_id: int,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    article = db.query(Article).filter(
        Article.author_id == current_user_id, 
        Article.id == article_id
    ).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# READ article by id
@router.get("/{article_id}", response_model=ArticleResponse)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("", response_model=ArticleResponse)
async def create_article(
    title: str = Form(...),
    content: str = Form(...),
    cover_image: UploadFile = File(None, alias="cover_image"),
    banners: List[UploadFile] = File(None, alias="banners[]"),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if banners:
        log.info(f"Received {len(banners)} banner(s)")
        for idx, f in enumerate(banners):
            log.info(f"→ Banner[{idx}] filename={f.filename}, content_type={f.content_type}")
    else:
        log.info("No banners uploaded")

    try:
        article = await ArticleService.create_article(
            db=db,
            author_id=current_user_id,
            title=title,
            content=content,
            cover_image=cover_image,
            banners=banners
        )

        log.info(f"✅ Article created with ID {article.id}")
        return article

    except Exception as e:
        log.error("❌ Error while creating article", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to create article: {str(e)}")

@router.put("/{article_id}")
async def update_article(
    article_id: int,
    title: str = Form(None),
    content: str = Form(None),
    cover_image: UploadFile = File(None),
    remove_banner_ids: str = Form(""),
    banners: List[UploadFile] = File(None, alias="banners[]"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    log.info(f"Current User: {current_user.id}")
    try:
        # convert string to list of ints: "1,2,3"
        remove_ids = (
            [int(i) for i in remove_banner_ids.split(",") if i.strip()]
            if remove_banner_ids else []
        )
        article = await ArticleService.update_article(
            db=db,
            article_id=article_id,
            author_id=current_user.id,
            title=title,
            content=content,
            image_cover=cover_image,
            banners=banners,
            remove_banner_ids=remove_ids,
        )

        return article
    except Exception as e:
        log.error("❌ Error while updating article", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to update article: {str(e)}")
    

@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id),
):
    return ArticleService.delete_article(
        db=db,
        article_id=article_id,
        author_id=current_user_id
    )
