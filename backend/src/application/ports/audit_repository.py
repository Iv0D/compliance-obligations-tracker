from typing import Protocol
from uuid import UUID

from src.domain.entities.audit_event import AuditEvent


class AuditRepository(Protocol):
    def save(self, event: AuditEvent) -> AuditEvent: ...

    def list_by_obligation_id(self, obligation_id: UUID) -> list[AuditEvent]: ...
