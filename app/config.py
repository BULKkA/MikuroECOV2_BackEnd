from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
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

    captcha_secret: str

    @field_validator("allowed_mime_types", mode="before")
    @classmethod
    def parse_mime_types(cls, v):
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v