from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from src.domain.entities.audit_event import AuditEvent
from src.domain.entities.obligation import Obligation
from src.domain.value_objects.obligation_type import ObligationType
from src.domain.value_objects.status import ObligationStatus


@dataclass(frozen=True)
class CreateObligationInput:
    type: ObligationType
    title: str
    owner: str
    due_date: date
    company_tax_id: str
    description: str | None = None
    requires_document: bool = False


@dataclass(frozen=True)
class UpdateObligationInput:
    type: ObligationType
    title: str
    owner: str
    due_date: date
    company_tax_id: str
    description: str | None = None
    requires_document: bool = False


@dataclass(frozen=True)
class ObligationDetail:
    obligation: Obligation
    audit_events: list[AuditEvent]
    valid_transitions: list[ObligationStatus]
    can_submit: bool
    is_overdue: bool
    company_tax_id_masked: str
    has_document: bool


@dataclass(frozen=True)
class DashboardKpis:
    total: int
    by_status: dict[ObligationStatus, int]
    overdue: int
    upcoming: int


@dataclass
class ObligationListItem:
    obligation: Obligation
    is_overdue: bool
    company_tax_id_masked: str
