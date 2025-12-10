from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config.app import app_config
from app.models import *
from .base import Base

DATABASE_URL = (
    f"mysql+pymysql://{app_config.DB_USERNAME}:{app_config.DB_PASSWORD}"
    f"@{app_config.DB_HOST}:{app_config.DB_PORT}/{app_config.DB_NAME}"
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()