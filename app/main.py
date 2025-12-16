import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
import uvicorn
import sys
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.app import app_config

# Middleware
from app.core.middleware.jwt import jwt_middleware
from app.core.middleware.logger import log_requests

from fastapi.staticfiles import StaticFiles

from app.database.base import Base
from app.database.session import engine

from app.routes.app import register_routes

Base.metadata.create_all(bind=engine)

# FastAPI Instance
app = FastAPI(
    title=app_config.APP_NAME,
    description=app_config.APP_DESC,
    version="1.0.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url="/docs", 
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTP Logging Middleware
@app.middleware("http")
async def add_log_requests(request, call_next):
    return await log_requests(request, call_next)

# original way
app.middleware("http")(log_requests)
app.middleware("http")(jwt_middleware)

# Register all routers
register_routes(app)

# Static Files
app.mount("/assets", StaticFiles(directory="app/assets"), name="assets")

print([m for m in sys.modules if "permission" in m])
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=app_config.APP_URL,
        port=app_config.APP_PORT,
        reload=True
    )