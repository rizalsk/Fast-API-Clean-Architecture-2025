from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FAST API"
    APP_DESC: str = "FAST API WEB API"
    APP_URL: str = "APP FAST API"
    APP_PORT: int = 5000
    
    DB_HOST: str
    DB_PORT: int = 3360
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    MAIL_HOST: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_ENCRYPTION: str = "tls"
    MAIL_FROM_ADDRESS: str = "admin@example.com"
    MAIL_FROM_NAME: str = "APP FAST API"

    class Config:
        env_file = ".env"

app_config = Settings()
