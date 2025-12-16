from fastapi import APIRouter
from sqlalchemy import text

from app.database.session import SessionLocal

router = APIRouter(tags=["Health"])

@router.get("/health")
def health_check():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()

        return {
            "status": "ok",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "disconnected",
            "detail": str(e)
        }
