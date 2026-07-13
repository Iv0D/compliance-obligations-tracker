from datetime import date

from src.domain.value_objects.status import ObligationStatus

_TERMINAL_STATUSES = frozenset({ObligationStatus.SUBMITTED, ObligationStatus.DONE})


def is_overdue(*, due_date: date, status: ObligationStatus, today: date) -> bool:
    return status not in _TERMINAL_STATUSES and due_date < today
