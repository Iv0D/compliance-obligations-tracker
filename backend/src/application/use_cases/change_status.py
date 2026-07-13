import logging
from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.application.errors import ConcurrencyConflictError, NotFoundError
from src.domain.entities.audit_event import AuditEvent
from src.domain.entities.obligation import Obligation
from src.domain.services.state_machine import ensure_can_transition
from src.domain.value_objects.status import ObligationStatus

logger = logging.getLogger(__name__)


class ChangeStatusUseCase:
    def __init__(
        self,
        obligation_repository,
        audit_repository,
        document_repository,
    ) -> None:
        self._obligations = obligation_repository
        self._audit = audit_repository
        self._documents = document_repository

    def execute(
        self,
        obligation_id: UUID,
        target_status: ObligationStatus,
        expected_version: int,
        *,
        changed_at: datetime | None = None,
    ) -> Obligation:
        obligation = self._obligations.get_by_id(obligation_id)
        if obligation is None:
            raise NotFoundError("obligation", str(obligation_id))
        if obligation.version != expected_version:
            raise ConcurrencyConflictError()

        has_document = self._documents.has_document_for_obligation(obligation_id)
        ensure_can_transition(
            current=obligation.status,
            target=target_status,
            requires_document=obligation.requires_document,
            has_document=has_document,
        )

        from_status = obligation.status
        obligation.status = target_status
        obligation.updated_at = datetime.now(timezone.utc)

        updated = self._obligations.update(obligation, expected_version)
        self._audit.save(
            AuditEvent.status_changed(
                event_id=uuid4(),
                obligation_id=obligation_id,
                from_status=from_status,
                to_status=target_status,
                changed_at=changed_at or datetime.now(timezone.utc),
            )
        )
        logger.info(
            "status_changed obligation=%s from=%s to=%s",
            obligation_id,
            from_status.value,
            target_status.value,
        )
        return updated
