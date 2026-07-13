from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.session import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    obligation_id: Mapped[UUID] = mapped_column(ForeignKey("obligations.id"))
    filename: Mapped[str] = mapped_column(String(255))
    mock_url: Mapped[str] = mapped_column(String(1024))
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
