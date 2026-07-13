from src.domain.value_objects.status import ObligationStatus


class DomainError(Exception):
    """Base class for domain rule violations."""


class InvalidCompanyTaxIdError(DomainError):
    """Raised when a company tax id does not meet the minimum shape."""


class InvalidStateTransitionError(DomainError):
    def __init__(self, current: ObligationStatus, target: ObligationStatus) -> None:
        self.current = current
        self.target = target
        super().__init__(f"invalid transition: {current.value} -> {target.value}")


class DocumentRequiredError(DomainError):
    def __init__(self) -> None:
        super().__init__("a document is required before submitting this obligation")
