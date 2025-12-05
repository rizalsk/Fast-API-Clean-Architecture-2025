import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from app.routes.api.auth.routes import router as auth_router
from app.routes.api.v1.article import router as article_router
from app.routes.api.v1.user import router as user_router
from app.routes.api.v1.banner import router as banner_router
from app.routes.api.v1.email import email_router

from fastapi.staticfiles import StaticFiles

from app.database.base import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Clean Architecture")

app.include_router(auth_router)
app.include_router(article_router)
app.include_router(user_router)
app.include_router(banner_router)
app.include_router(email_router)

app.mount("/assets", StaticFiles(directory="app/assets"), name="assets")
