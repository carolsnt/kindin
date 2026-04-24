"""Auth schemas."""
from pydantic import BaseModel


class TelegramAuthPayload(BaseModel):
    """Telegram Login Widget payload."""

    id: int
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    auth_date: int
    hash: str


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"
    user_id: str
