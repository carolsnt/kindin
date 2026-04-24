"""Application settings loaded from environment variables."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Kindin API configuration."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Database
    DATABASE_URL: str = "postgresql+psycopg://kindin:kindin@localhost:5432/kindin"

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"

    # JWT
    JWT_SECRET: str = "changeme-supersecret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # SMTP
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASS: str = ""
    SMTP_FROM: str = "noreply@example.com"

    # Telegram
    TELETHON_SESSION_PATH: str = "./kindin.session"
    TELEGRAM_API_ID: int = 0
    TELEGRAM_API_HASH: str = ""
    TELEGRAM_BOT_TOKEN: str = ""

    # Limits
    MAX_FILE_SIZE_MB: int = 25
    SHARE_LINK_TTL_HOURS: int = 24

    # Rate limiting (requests per window)
    RATE_LIMIT_SEARCHES_PER_MINUTE: int = 10
    RATE_LIMIT_DOWNLOADS_PER_HOUR: int = 50

    # Environment
    ENV: str = "development"


settings = Settings()
