from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.value_objects.status import ObligationStatus
from src.infrastructure.database.session import Base


class AuditEventModel(Base):
    __tablename__ = "audit_events"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    obligation_id: Mapped[UUID] = mapped_column(ForeignKey("obligations.id"))
    from_status: Mapped[ObligationStatus] = mapped_column(
        Enum(ObligationStatus, native_enum=False, length=20)
    )
    to_status: Mapped[ObligationStatus] = mapped_column(
        Enum(ObligationStatus, native_enum=False, length=20)
    )
    changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
