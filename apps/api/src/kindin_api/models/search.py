"""Search model."""
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from kindin_api.db import Base


class Search(Base):
    """A book search initiated by a user."""

    __tablename__ = "searches"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    query_title: Mapped[str | None] = mapped_column(Text, nullable=True)
    query_author: Mapped[str | None] = mapped_column(Text, nullable=True)
    query_format: Mapped[str] = mapped_column(Text, nullable=False)  # any|epub|mobi|pdf
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="running")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)
