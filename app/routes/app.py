from fastapi import FastAPI

# Health
from app.routes.health import router as health_router

# Web
from app.routes.web import router as web_router

# Auth
from app.routes.api.auth.routes import router as auth_router

# API v1
from app.routes.api.v1.article import router as article_router
from app.routes.api.v1.user import router as user_router
from app.routes.api.v1.banner import router as banner_router
from app.routes.api.v1.email import email_router

# Permission module
from app.modules.permission.routes.permission import router as permission_router
from app.modules.permission.routes.guarded_router import router as guarded_router


def register_routes(app: FastAPI):
    app.include_router(web_router)
    app.include_router(health_router)
    app.include_router(auth_router)

    # Prefix API V1 Group
    api_v1_routes = [
        article_router,
        user_router,
        banner_router,
        email_router,
        permission_router,
        guarded_router
    ]

    for router in api_v1_routes:
        app.include_router(
            router,
            prefix="/api/v1",
        )
