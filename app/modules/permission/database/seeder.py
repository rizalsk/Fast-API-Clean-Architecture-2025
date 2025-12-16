from app.database.session import SessionLocal

from .factories.permissions import seed_permissions
from .factories.groups import seed_permission_groups
from .factories.roles import seed_roles
from .factories.role_permissions import seed_role_permissions
from .factories.role_groups import seed_role_groups
from .factories.user_roles import seed_user_roles
from .factories.user_permissions import seed_user_permissions
from .factories.permission_group_permissions import seed_permission_group_permissions
from sqlalchemy.exc import IntegrityError

def run_seeder():
    db = SessionLocal()
    print("Seeding permissions...")
    seed_permissions(db)

    print("Seeding permission groups...")
    seed_permission_groups(db)

    print("Seeding roles...")
    seed_roles(db)

    print("Seeding role → permissions...")
    seed_role_permissions(db)

    print("Seeding role → groups...")
    seed_role_groups(db)

    print("Seeding user → roles...")
    seed_user_roles(db)

    print("Seeding user → permissions...")
    seed_user_permissions(db)

    print("Seeding permission group → permissions...")
    seed_permission_group_permissions(db)

    db.commit()
    db.close()
    print("Permission Seeder completed successfully!")
    # try:

    # except IntegrityError:
    #     db.rollback()
    #     print("Permission Seeder failed!")
    
