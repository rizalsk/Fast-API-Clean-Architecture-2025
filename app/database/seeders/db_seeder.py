# app\database\seeders\db_seeder.py
# app/database/seeders/db_seeder.py

from app.database.session import SessionLocal
from app.database.factories.first_factory import (
    seed_articles,
    seed_banners,
    seed_users
)

def run_seeder():
    db = SessionLocal()
    try:
        users = seed_users(db)
        articles = seed_articles(db, users)
        seed_banners(db, articles)
    finally:
        db.close()

if __name__ == "__main__":
    run_seeder()
