"""Search schemas."""
import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class SearchCreate(BaseModel):
    title: str | None = None
    author: str | None = None
    format: Literal["any", "epub", "mobi", "pdf"] = "any"


class SearchResponse(BaseModel):
    id: uuid.UUID
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class SearchResultResponse(BaseModel):
    id: uuid.UUID
    filename: str
    format: str
    file_size: int | None = None
    title_raw: str | None = None
    author_raw: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class PaginatedResults(BaseModel):
    items: list[SearchResultResponse]
    total: int
    page: int
    per_page: int
