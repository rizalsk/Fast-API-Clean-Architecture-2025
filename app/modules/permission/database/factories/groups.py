from app.modules.permission.models.permission_group import PermissionGroup

def seed_permission_groups(db):
    data = [
        {"id": 1, "name": "Manage User"},
        {"id": 2, "name": "Manage Article"},
        {"id": 3, "name": "Manage Banner"},
    ]

    for item in data:
        exists = db.query(PermissionGroup).filter(PermissionGroup.id == item["id"]).first()
        if not exists:
            db.add(PermissionGroup(**item))
    db.commit()
