from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from src.domain.value_objects.company_tax_id import CompanyTaxId
from src.domain.value_objects.obligation_type import ObligationType
from src.domain.value_objects.status import ObligationStatus


@dataclass
class Obligation:
    id: UUID
    type: ObligationType
    title: str
    owner: str
    due_date: date
    company_tax_id: CompanyTaxId
    status: ObligationStatus = ObligationStatus.PENDING
    description: str | None = None
    requires_document: bool = False
    version: int = 1
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
