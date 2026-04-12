from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://Mikuro_admin_db:Sergosergo666!@localhost:5432/Mikuro_db"
    
    # JWT
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Media
    media_upload_path: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_mime_types: List[str] = ["image/jpeg", "image/png", "image/gif"]
    
    # Captcha
    captcha_secret: str = "captcha-secret"
    
    class Config:
        env_file = ".env"

settings = Settings()