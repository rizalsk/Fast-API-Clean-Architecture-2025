# app\database\seeders\first_seeder.py
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.article import Article
from app.models.banner_image import BannerImage
from app.core.security import hash_password
import os

UPLOAD_DIR = "app/assets/uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def seed_users(db: Session):
    users_data = [
        {"username": "admin", "email": "admin@mail.com", "name": "Admin", "password": "password", "avatar": "adminavatar.jpg"},
        {"username": "bob", "email": "bob@mail.com", "name": "Bob", "password": "password", "avatar": "bobavatar.jpg"},
        {"username": "alice", "email": "alice@mail.com", "name": "Alice", "password": "password", "avatar": "aliceavatar.jpg"},
    ]
    users = []
    for u in users_data:
        hashed = hash_password(u["password"])
        file_path = os.path.join(UPLOAD_DIR, u["avatar"])
        with open(file_path, "wb") as f:
            f.write(b"")  # empty file for demo
        user = User(username=u["username"], email=u["email"], name=u["name"], password=hashed, avatar=file_path)
        db.add(user)
        users.append(user)
    db.commit()
    for user in users:
        db.refresh(user)
    print(f"Seeded {len(users)} users")
    return users

def seed_articles(db: Session, users):
    articles_data = [
        {
            "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit", 
            "content": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto", 
            "cover_image": 'cover_image1.jpg',
            "author_id": users[0].id
        },
        {
            "title": "qui est esse", 
            "content": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla", 
            "cover_image": 'cover_image2.jpg',
            "author_id": users[1].id
        },
        {
            "title": "Big Savings in India Gives Tesla Stock (NASDAQ:TSLA) a Small Boost", 
            "content": "Electric vehicle giant Tesla (TSLA) is working hard to build interest for its product line in India, and turning to one of the most tried-and-true methods around: pointing out cost savings. It turns out that Indian buyers can recoup about a third of the cost", 
            "cover_image": 'cover_image3.jpg',
            "author_id": users[1].id
        },
        {
            "title": "Tesla Picks Suppliers by Quality, Not Country, Executive Says", 
            "content": "Tesla India aims to differentiate itself from other luxury EV makers through easy Supercharger access, on-the-spot remote diagnostics and practically service-free ownership, according to Shashank Srivastava, head of Tesla India and South Asia. ", 
            "cover_image": 'cover_image4.jpg',
            "author_id": users[1].id
        },
        {
            "title": "Cathie Wood Dumps $11.6 Million Worth Of Tesla Stock: Here Is What Ark Purchased Instead", 
            "content": "On Wednesday, Cathie Wood-led Ark Invest made significant trades involving Tesla Inc. (NASDAQ:TSLA), Coinbase Global Inc. (NASDAQ:COIN), and Deere &amp; Co. (NYSE:DE). These trades were part of Arks … [+140 chars]", 
            "cover_image": 'cover_image5.jpg',
            "author_id": users[1].id
        },
    ]
    articles = []
    for a in articles_data:
        file_path = os.path.join(UPLOAD_DIR, a["cover_image"])
        with open(file_path, "wb") as f:
            f.write(b"")  # empty file for demo
        article = Article(title=a["title"], content=a["content"], author_id=a["author_id"], cover_image=file_path)
        db.add(article)
        articles.append(article)
    db.commit()
    for article in articles:
        db.refresh(article)
    print(f"Seeded {len(articles)} articles")
    return articles

def seed_banners(db: Session, articles):
    # Create dummy banners (empty files for demo)
    banners_data = [
        {"article_id": articles[0].id, "filename": "banner1.jpg"},
        {"article_id": articles[1].id, "filename": "banner2.jpg"},
        {"article_id": articles[2].id, "filename": "banner3.jpg"},
        {"article_id": articles[3].id, "filename": "banner4.jpg"},
        {"article_id": articles[4].id, "filename": "banner5.jpg"},
    ]
    banners = []
    for b in banners_data:
        file_path = os.path.join(UPLOAD_DIR, b["filename"])
        with open(file_path, "wb") as f:
            f.write(b"")  # empty file for demo
        banner = BannerImage(article_id=b["article_id"], file_path=file_path, filename=b["filename"])
        db.add(banner)
        banners.append(banner)
    db.commit()
    for banner in banners:
        db.refresh(banner)
    print(f"Seeded {len(banners)} banners")
    return banners