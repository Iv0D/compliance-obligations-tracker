from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.domain.value_objects.status import ObligationStatus


@dataclass
class AuditEvent:
    id: UUID
    obligation_id: UUID
    from_status: ObligationStatus
    to_status: ObligationStatus
    changed_at: datetime

    @classmethod
    def status_changed(
        cls,
        *,
        event_id: UUID,
        obligation_id: UUID,
        from_status: ObligationStatus,
        to_status: ObligationStatus,
        changed_at: datetime,
    ) -> "AuditEvent":
        return cls(
            id=event_id,
            obligation_id=obligation_id,
            from_status=from_status,
            to_status=to_status,
            changed_at=changed_at,
        )
