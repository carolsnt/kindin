"""SendJob schemas."""
import uuid
from datetime import datetime

from pydantic import BaseModel


class SendJobCreate(BaseModel):
    destination_id: uuid.UUID
    result_ids: list[uuid.UUID]


class SendJobResponse(BaseModel):
    id: uuid.UUID
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SendJobItemResponse(BaseModel):
    id: uuid.UUID
    search_result_id: uuid.UUID
    status: str
    error_message: str | None = None

    model_config = {"from_attributes": True}
