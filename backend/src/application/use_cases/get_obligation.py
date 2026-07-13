from datetime import date, datetime, timezone
from uuid import UUID, uuid4

from src.application.dtos.obligation_dto import ObligationDetail
from src.application.errors import NotFoundError
from src.domain.entities.obligation import Obligation
from src.domain.services.overdue import is_overdue
from src.domain.services.state_machine import ensure_can_transition
from src.domain.value_objects.status import ALLOWED_TRANSITIONS, ObligationStatus


class GetObligationUseCase:
    def __init__(
        self,
        obligation_repository,
        audit_repository,
        document_repository,
    ) -> None:
        self._obligations = obligation_repository
        self._audit = audit_repository
        self._documents = document_repository

    def execute(self, obligation_id: UUID, *, today: date | None = None) -> ObligationDetail:
        obligation = self._obligations.get_by_id(obligation_id)
        if obligation is None:
            raise NotFoundError("obligation", str(obligation_id))

        today = today or date.today()
        has_document = self._documents.has_document_for_obligation(obligation_id)
        valid_transitions = sorted(
            ALLOWED_TRANSITIONS[obligation.status],
            key=lambda status: status.value,
        )

        return ObligationDetail(
            obligation=obligation,
            audit_events=self._audit.list_by_obligation_id(obligation_id),
            valid_transitions=valid_transitions,
            can_submit=_can_submit(obligation, has_document),
            is_overdue=is_overdue(
                due_date=obligation.due_date,
                status=obligation.status,
                today=today,
            ),
            company_tax_id_masked=obligation.company_tax_id.masked(),
            has_document=has_document,
        )


def _can_submit(obligation: Obligation, has_document: bool) -> bool:
    if ObligationStatus.SUBMITTED not in ALLOWED_TRANSITIONS[obligation.status]:
        return False
    if obligation.requires_document and not has_document:
        return False
    try:
        ensure_can_transition(
            current=obligation.status,
            target=ObligationStatus.SUBMITTED,
            requires_document=obligation.requires_document,
            has_document=has_document,
        )
    except Exception:
        return False
    return True
