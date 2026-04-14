from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",          # добавь это
        env_file_encoding="utf-8", # и это
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

    allowed_mime_types: list[str] = []

    captcha_secret: str = ""  # опциональное

    @field_validator("allowed_mime_types", mode="before")
    @classmethod
    def parse_mime_types(cls, v):
        if isinstance(v, str):
            # поддержка обоих форматов: "a,b,c" и ["a","b","c"]
            if v.startswith("["):
                import json
                return json.loads(v)
            return [x.strip() for x in v.split(",")]
        return v

settings = Settings()