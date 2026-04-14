from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7

    media_upload_path: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024

    allowed_mime_types: str = "image/jpeg,image/png,image/gif"  # str, не list

    captcha_secret: str = ""

    def get_allowed_mime_types(self) -> List[str]:
        v = self.allowed_mime_types.strip()
        if v.startswith("["):
            import json
            return json.loads(v)
        return [x.strip() for x in v.split(",") if x.strip()]


settings = Settings()