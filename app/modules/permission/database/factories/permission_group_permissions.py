from app.modules.permission.models.permission_group_permission import PermissionGroupPermission

def seed_permission_group_permissions(db):
    data = [
        {"group_id": 1, "permission_id": 1},
        {"group_id": 1, "permission_id": 2},
        {"group_id": 1, "permission_id": 3},
    ]

    for item in data:
        exists = db.query(PermissionGroupPermission).filter(
            PermissionGroupPermission.group_id == item["group_id"],
            PermissionGroupPermission.permission_id == item["permission_id"],
        ).first()

        if not exists:
            db.add(PermissionGroupPermission(**item))

    db.commit()
