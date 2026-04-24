"""SearchResult model."""
import uuid
from datetime import datetime

from sqlalchemy import BigInteger, ForeignKey, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from kindin_api.db import Base


class SearchResult(Base):
    """A single file found during a search."""

    __tablename__ = "search_results"
    __table_args__ = (
        UniqueConstraint(
            "search_id", "source_id", "telegram_message_id", "telegram_file_id",
            name="uq_search_results_composite",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    search_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("searches.id"), nullable=False)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)
    telegram_message_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    telegram_file_id: Mapped[str] = mapped_column(Text, nullable=False)
    filename: Mapped[str] = mapped_column(Text, nullable=False)
    format: Mapped[str] = mapped_column(Text, nullable=False)  # epub|mobi|pdf|other
    file_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    title_raw: Mapped[str | None] = mapped_column(Text, nullable=True)
    author_raw: Mapped[str | None] = mapped_column(Text, nullable=True)
    sha256: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
