from app.modules.permission.models.role_permission import RolePermission

def seed_role_permissions(db):
    data = [
        # Administrator
        {"role_id": 1, "permission_id": 1},
        {"role_id": 1, "permission_id": 2},
        {"role_id": 1, "permission_id": 3},
        {"role_id": 1, "permission_id": 4},
        {"role_id": 1, "permission_id": 5},

        # Editor
        {"role_id": 2, "permission_id": 1},
        {"role_id": 2, "permission_id": 2},
        {"role_id": 2, "permission_id": 3},
        {"role_id": 2, "permission_id": 5},

        # Viewer
        {"role_id": 3, "permission_id": 2},
    ]

    for item in data:
        exists = db.query(RolePermission).filter(
            RolePermission.role_id == item["role_id"],
            RolePermission.permission_id == item["permission_id"]
        ).first()

        if not exists:
            db.add(RolePermission(**item))

    db.commit()
