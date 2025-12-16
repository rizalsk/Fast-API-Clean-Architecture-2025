from app.modules.permission.models.role import Role

def seed_roles(db):
    data = [
        {"id": 1, "name": "Administrator"},
        {"id": 2, "name": "Editor"},
        {"id": 3, "name": "Viewer"},
    ]

    for item in data:
        exists = db.query(Role).filter(Role.id == item["id"]).first()
        if not exists:
            db.add(Role(**item))
    db.commit()
