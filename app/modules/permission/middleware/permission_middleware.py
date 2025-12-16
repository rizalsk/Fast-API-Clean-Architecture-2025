from fastapi import Request, HTTPException, Depends, status
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from app.modules.permission.models.user_permission import UserPermission
from app.modules.permission.models.permission_group import PermissionGroup
from app.modules.permission.models.permission import Permission
from app.database.session import get_db
from typing import Callable
from app.core.jwt import verify_token
from app.dependencies.auth import get_current_user_id, get_current_user
from app.models.user import User

class PermissionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db: Session, required_permissions: list):
        super().__init__(app)
        self.db = db
        self.required_permissions = required_permissions

    async def dispatch(self, request: Request, call_next):
        user = getattr(request.state, "user", None)
        if not user:
            raise HTTPException(status_code=401, detail="Unauthorized Permission!")

        # Ambil permission user dari DB
        user_perms = (
            self.db.query(UserPermission)
            .join(Permission, UserPermission.permission_id == Permission.id)
            .join(PermissionGroup, UserPermission.group_id == PermissionGroup.id)
            .filter(UserPermission.user_id == user.id)
            .all()
        )

        # Cek permission
        has_permission = False
        for perm in self.required_permissions:
            for up in user_perms:
                if up.permission.name == perm["name"] and up.group.name == perm["group"]:
                    has_permission = True
                    break
            if has_permission:
                break

        if not has_permission:
            raise HTTPException(status_code=403, detail="Forbidden")

        response = await call_next(request)
        return response


def has_access(permission_str: str):
    """
    Middleware user check.
    Format:
    - "Group:Permission" -> contoh: "Manage User:view"
    - "Permission" -> contoh: "view" (tanpa group)
    """
    def dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db),
    ):

        if ":" in permission_str:
            group_name, perm_name = permission_str.split(":")
        else:
            group_name, perm_name = None, permission_str

        # Ambil permission user dari table user_permissions
        user_permissions = get_user_permissions(current_user.id, db)

        # Cek apakah user memiliki permission
        has_perm = False
        for p in user_permissions:
            if group_name:
                if p["name"] == perm_name and p.get("group") and p["group"]["name"] == group_name:
                    has_perm = True
                    break
            else:
                if p["name"] == perm_name:
                    has_perm = True
                    break

        if not has_perm:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied, No Permission allowed!")
        return True

    return dependency


def get_user_permissions(user_id: int, db: Session) -> list:
    results = (
        db.query(UserPermission, Permission, PermissionGroup)
        .join(Permission, UserPermission.permission_id == Permission.id)
        .outerjoin(PermissionGroup, UserPermission.group_id == PermissionGroup.id)
        .filter(UserPermission.user_id == user_id)
        .all()
    )

    permissions = []

    for up, perm, group in results:
        permissions.append({
            "id": perm.id,
            "name": perm.name,
            "is_default": perm.is_default,
            "group": {
                "id": group.id,
                "name": group.name,
            } if group else None
        })

    return permissions