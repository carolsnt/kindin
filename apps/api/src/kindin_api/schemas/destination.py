"""Destination schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class DestinationCreate(BaseModel):
    type: str  # kindle_email | email
    value: str
    label: str
    is_default: bool = False


class DestinationUpdate(BaseModel):
    label: str | None = None
    value: str | None = None
    is_default: bool | None = None


class DestinationResponse(BaseModel):
    id: uuid.UUID
    type: str
    value: str
    label: str
    is_default: bool
    created_at: datetime

    model_config = {"from_attributes": True}
