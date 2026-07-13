from datetime import date, datetime

from pydantic import BaseModel

from src.domain.value_objects.obligation_type import ObligationType
from src.domain.value_objects.status import ObligationStatus


class ObligationSummaryResponse(BaseModel):
    id: str
    type: ObligationType
    title: str
    owner: str
    due_date: date
    status: ObligationStatus
    description: str | None
    requires_document: bool
    company_tax_id_masked: str
    is_overdue: bool
    version: int
    created_at: datetime | None
    updated_at: datetime | None


class AuditEventResponse(BaseModel):
    from_status: ObligationStatus
    to_status: ObligationStatus
    changed_at: datetime


class ObligationDetailResponse(ObligationSummaryResponse):
    audit_events: list[AuditEventResponse]
    valid_transitions: list[ObligationStatus]
    can_submit: bool
    has_document: bool


class DocumentResponse(BaseModel):
    id: str
    obligation_id: str
    filename: str
    mock_url: str
    created_at: datetime | None


class DashboardResponse(BaseModel):
    total: int
    by_status: dict[ObligationStatus, int]
    overdue: int
    upcoming: int


class ErrorBody(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorBody
