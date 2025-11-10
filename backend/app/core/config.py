from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    app_name: str = "Photo Guide API"
    app_version: str = "1.0.0"
    api_prefix: str = "/api/v1"

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Google Gemini API
    google_api_key: str = ""
    gemini_model: str = "gemini-2.0-flash-exp"

    # File Upload
    max_upload_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: set = {".jpg", ".jpeg", ".png", ".webp"}
    upload_dir: str = "uploads"
    output_dir: str = "outputs"

    # Analysis Settings
    analysis_timeout: int = 5  # seconds
    generation_timeout: int = 30  # seconds

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
