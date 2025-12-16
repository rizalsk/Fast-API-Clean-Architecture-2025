from app.modules.permission.models.user_role import UserRole

def seed_user_roles(db):
    data = [
        {"user_id": 1, "role_id": 1},   # admin → Administrator
        {"user_id": 2, "role_id": 2},   # editor → Editor
        {"user_id": 3, "role_id": 3},   # viewer → Viewer
    ]

    for item in data:
        exists = db.query(UserRole).filter(
            UserRole.user_id == item["user_id"],
            UserRole.role_id == item["role_id"],
        ).first()

        if not exists:
            db.add(UserRole(**item))

    db.commit()
