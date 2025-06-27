import os
from dotenv import load_dotenv

load_dotenv()

class Settings():
    PROJECT_NAME: str = "SilentScribe"
    DEBUG: bool = True
    DATABASE_URL: str = os.getenv("SQLALCHEMY_DATABASE_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24

settings = Settings()