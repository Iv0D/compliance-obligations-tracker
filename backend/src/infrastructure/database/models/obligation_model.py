from datetime import date, datetime
from uuid import UUID

from sqlalchemy import Boolean, Date, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.value_objects.obligation_type import ObligationType
from src.domain.value_objects.status import ObligationStatus
from src.infrastructure.database.session import Base


class ObligationModel(Base):
    __tablename__ = "obligations"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    type: Mapped[ObligationType] = mapped_column(
        Enum(ObligationType, native_enum=False, length=50)
    )
    title: Mapped[str] = mapped_column(String(255))
    owner: Mapped[str] = mapped_column(String(255))
    due_date: Mapped[date] = mapped_column(Date)
    company_tax_id: Mapped[str] = mapped_column(String(50))
    status: Mapped[ObligationStatus] = mapped_column(
        Enum(ObligationStatus, native_enum=False, length=20)
    )
    description: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    requires_document: Mapped[bool] = mapped_column(Boolean, default=False)
    version: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
