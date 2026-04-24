"""SendJob and SendJobItem models."""
import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from kindin_api.db import Base


class SendJob(Base):
    """Async job to send files by e-mail."""

    __tablename__ = "send_jobs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    destination_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("destinations.id"), nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="queued")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)


class SendJobItem(Base):
    """Individual file within a send job."""

    __tablename__ = "send_job_items"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("send_jobs.id"), nullable=False)
    search_result_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("search_results.id"), nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, server_default="queued")
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
