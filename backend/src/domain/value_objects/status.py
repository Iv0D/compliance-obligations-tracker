from enum import Enum


class ObligationStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"
    DONE = "done"


ALLOWED_TRANSITIONS: dict[ObligationStatus, frozenset[ObligationStatus]] = {
    ObligationStatus.PENDING: frozenset({ObligationStatus.IN_PROGRESS}),
    ObligationStatus.IN_PROGRESS: frozenset(
        {ObligationStatus.SUBMITTED, ObligationStatus.PENDING}
    ),
    ObligationStatus.SUBMITTED: frozenset(
        {ObligationStatus.DONE, ObligationStatus.IN_PROGRESS}
    ),
    ObligationStatus.DONE: frozenset({ObligationStatus.IN_PROGRESS}),
}
