from fastapi import Request, HTTPException, status
from app.core.jwt import verify_token
from fastapi.responses import JSONResponse
from jose import JWTError

EXCLUDE_PATHS = [
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/auth/login",
    "/auth/register",
    "/auth/refresh",
    "/v1/articles",
]

async def jwt_middleware(request: Request, call_next):
    if request.url.path in EXCLUDE_PATHS:
        return await call_next(request)

    auth = request.headers.get("Authorization")

    if not auth:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": "Unauthorized",
                "error": "Missing Authorization header"
            }
        )

    if not auth.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": "Unauthorized",
                "error": "Invalid Authorization format"
            }
        )

    token = auth.replace("Bearer ", "")

    try:
        payload = verify_token(token)
        request.state.user = payload  # optional
    except JWTError as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "success": False,
                "message": "Unauthorized",
                "error": "Invalid or expired token"
            }
        )

    return await call_next(request)

