from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="BOXING_",
        extra="ignore",
    )

    app_name: str = "Boxing Fight Analysis API"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    docs_enabled: bool = True
    cors_origins: list[str] = Field(default_factory=lambda: ["http://localhost:5173"])

    data_dir: Path = BACKEND_DIR / "data"
    database_url: str = f"sqlite+aiosqlite:///{BACKEND_DIR / 'data' / 'app.db'}"
    max_upload_bytes: int = 2 * 1024 * 1024 * 1024
    upload_chunk_bytes: int = 1024 * 1024
    allowed_video_extensions: set[str] = Field(
        default_factory=lambda: {".avi", ".m4v", ".mkv", ".mov", ".mp4", ".webm"}
    )
    allowed_video_content_types: set[str] = Field(
        default_factory=lambda: {
            "application/octet-stream",
            "video/avi",
            "video/mp4",
            "video/quicktime",
            "video/webm",
            "video/x-m4v",
            "video/x-matroska",
            "video/x-msvideo",
        }
    )

    @property
    def upload_dir(self) -> Path:
        return self.data_dir / "uploads"

    def ensure_directories(self) -> None:
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
