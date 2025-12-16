from app.modules.permission.models.role_group import RoleGroup

def seed_role_groups(db):
    data = [
        {"role_id": 1, "group_id": 1},  # Admin → Manage User
        {"role_id": 1, "group_id": 2},
        {"role_id": 1, "group_id": 3},

        {"role_id": 2, "group_id": 2},  # Editor → Manage Article
        {"role_id": 2, "group_id": 3},
    ]

    for item in data:
        exists = db.query(RoleGroup).filter(
            RoleGroup.role_id == item["role_id"],
            RoleGroup.group_id == item["group_id"]
        ).first()

        if not exists:
            db.add(RoleGroup(**item))

    db.commit()
