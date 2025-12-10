from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.core.config.app import app_config

def create_access_token(data: dict):
    expire = datetime.now() + timedelta(
        minutes=app_config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload = data.copy()
    payload.update({"exp": expire})
    return jwt.encode(payload, app_config.JWT_SECRET, algorithm=app_config.JWT_ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.now() + timedelta(
        days=app_config.REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload = data.copy()
    payload.update({"exp": expire})
    return jwt.encode(payload, app_config.JWT_SECRET, algorithm=app_config.JWT_ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, app_config.JWT_SECRET, algorithms=[app_config.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
    
def decode_access_token(token: str):
    try:
        return jwt.decode(token, app_config.JWT_SECRET, algorithms=[app_config.JWT_ALGORITHM])
    except Exception:
        return None