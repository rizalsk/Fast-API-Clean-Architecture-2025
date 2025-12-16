from app.modules.permission.models.user_permission import UserPermission

def seed_user_permissions(db):
    data = [
        {"user_id": 1, "group_id": 1, "permission_id": 1},
        {"user_id": 1, "group_id": 1, "permission_id": 2},
        {"user_id": 1, "group_id": 1, "permission_id": 3},
        {"user_id": 1, "group_id": 1, "permission_id": 4},
        {"user_id": 1, "group_id": 2, "permission_id": 1},
        {"user_id": 1, "group_id": 2, "permission_id": 2},
        {"user_id": 1, "group_id": 2, "permission_id": 3},
        {"user_id": 1, "group_id": 2, "permission_id": 4},
        {"user_id": 1, "group_id": 3, "permission_id": 1},
        {"user_id": 1, "group_id": 3, "permission_id": 2},
        {"user_id": 1, "group_id": 3, "permission_id": 3},
        {"user_id": 1, "group_id": 3, "permission_id": 4},
        {"user_id": 2, "group_id": 2, "permission_id": 1},
        {"user_id": 2, "group_id": 2, "permission_id": 2},
        {"user_id": 2, "group_id": 2, "permission_id": 3},
        {"user_id": 2, "group_id": 2, "permission_id": 4},
        {"user_id": 3, "group_id": None, "permission_id": 3}, # Direct permission without group
    ]

    for item in data:
        exists = db.query(UserPermission).filter(
            UserPermission.user_id == item["user_id"],
            UserPermission.group_id == item["group_id"],
            UserPermission.permission_id == item["permission_id"],
        ).first()

        if not exists:
            db.add(UserPermission(**item))

    db.commit()
