from sqlalchemy.orm import Session, joinedload
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.modules.permission.models.user_permission import UserPermission
from app.schemas.user import UserCreate
from app.modules.permission.schemas.user_schema import PermissionSchema, UserResponse
from sqlalchemy import text

class UserService:

    @staticmethod
    def list_users(db: Session):
        users = (
            db.query(User)
            .options(
                joinedload(User.roles),
                joinedload(User.user_permissions)
                    .joinedload(UserPermission.permission),
                joinedload(User.user_permissions)
                    .joinedload(UserPermission.group),
            )
            .all()
        )

        result = []
        for u in users:
            permissions = [up.permission for up in u.user_permissions]
            for idx, up in enumerate(u.user_permissions):
                group_name = up.group.name if up.group else None
                route_group = (
                    f"{group_name}:{up.permission.name}"
                    if group_name
                    else up.permission.name
                )
                permissions[idx].route_group = route_group
                permissions[idx].group = up.group

            user_schema = UserResponse.model_validate(u)
            user_schema.permissions = [PermissionSchema.model_validate(p) for p in permissions]
            result.append(user_schema)

        return result
    
    @staticmethod
    def create_user(db: Session, payload: UserCreate):
        user = User(
            username=payload.username,
            email=payload.email,
            name=payload.name,
            password=payload.password
        )
        return UserRepository.create(db, user, payload.role_ids)

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = UserRepository.find_by_id(db, user_id)
        if user:
            UserRepository.delete(db, user)
        return user
