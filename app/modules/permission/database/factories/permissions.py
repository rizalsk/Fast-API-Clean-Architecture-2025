from app.modules.permission.models.permission import Permission

def seed_permissions(db):
    data = [
        {"id": 1, "name": "create", "is_default": True},
        {"id": 2, "name": "view",   "is_default": True},
        {"id": 3, "name": "edit",   "is_default": True},
        {"id": 4, "name": "delete", "is_default": True},
        {"id": 5, "name": "upload", "is_default": False},
    ]

    for item in data:
        exists = db.query(Permission).filter(Permission.id == item["id"]).first()
        if not exists:
            db.add(Permission(**item))
    db.commit()
