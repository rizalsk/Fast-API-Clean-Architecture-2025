from fastapi import Request, HTTPException
from app.modules.permission.services.permission_service import PermissionService
from sqlalchemy.orm import Session
from app.database.session import SessionLocal

def permission_required(permission_name: str, group_id: int = None):
    def wrapper(func):
        async def decorated(request: Request, *args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Token missing")
            
            from app.core.jwt import verify_token
            payload = verify_token(token)
            if not payload:
                raise HTTPException(status_code=401, detail="Invalid token")
            
            user_id = payload.get("user_id")
            db: Session = SessionLocal()
            service = PermissionService(db)
            has_perm = service.has_permission(user_id, permission_name, group_id)
            db.close()
            if not has_perm:
                raise HTTPException(status_code=403, detail="Permission denied")
            return await func(request, *args, **kwargs)
        return decorated
    return wrapper
