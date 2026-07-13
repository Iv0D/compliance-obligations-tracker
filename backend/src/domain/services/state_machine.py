from src.domain.errors.domain_errors import (
    DocumentRequiredError,
    InvalidStateTransitionError,
)
from src.domain.value_objects.status import ALLOWED_TRANSITIONS, ObligationStatus


def ensure_can_transition(
    *,
    current: ObligationStatus,
    target: ObligationStatus,
    requires_document: bool,
    has_document: bool,
) -> None:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise InvalidStateTransitionError(current, target)
    if target is ObligationStatus.SUBMITTED and requires_document and not has_document:
        raise DocumentRequiredError()
