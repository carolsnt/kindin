"""Source schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class SourceCreate(BaseModel):
    type: str  # telegram_channel | telegram_group
    telegram_chat_id: int
    name: str
    is_active: bool = True


class SourceUpdate(BaseModel):
    name: str | None = None
    is_active: bool | None = None


class SourceResponse(BaseModel):
    id: uuid.UUID
    type: str
    telegram_chat_id: int
    name: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}
