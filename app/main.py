import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI, Request
import uvicorn
import time
from app.core.config.app import app_config
from app.core.middleware.http import log_requests

from app.routes.web import router as web_router
from app.routes.api.auth.routes import router as auth_router
from app.routes.api.v1.article import router as article_router
from app.routes.api.v1.user import router as user_router
from app.routes.api.v1.banner import router as banner_router
from app.routes.api.v1.email import email_router


from fastapi.staticfiles import StaticFiles

from app.database.base import Base
from app.database.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=app_config.APP_NAME,
    description=app_config.APP_DESC,
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url="/docs", 
    redoc_url="/redoc"
)

@app.middleware("http")
async def add_log_requests(request, call_next):
    return await log_requests(request, call_next)


app.include_router(web_router)
app.include_router(auth_router)
app.include_router(article_router)
app.include_router(user_router)
app.include_router(banner_router)
app.include_router(email_router)

# app.include_router(permission_router)
# app.include_router(permission_subrouter)

app.mount("/assets", StaticFiles(directory="app/assets"), name="assets")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=app_config.APP_URL,
        port=app_config.APP_PORT,
        reload=True
    )