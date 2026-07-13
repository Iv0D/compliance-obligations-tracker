from datetime import datetime, timezone
from uuid import uuid4

from src.application.dtos.obligation_dto import CreateObligationInput
from src.domain.entities.obligation import Obligation
from src.domain.value_objects.company_tax_id import CompanyTaxId


class CreateObligationUseCase:
    def __init__(self, obligation_repository) -> None:
        self._obligations = obligation_repository

    def execute(self, data: CreateObligationInput) -> Obligation:
        if not data.title.strip():
            raise ValueError("title is required")
        if not data.owner.strip():
            raise ValueError("owner is required")

        now = datetime.now(timezone.utc)
        obligation = Obligation(
            id=uuid4(),
            type=data.type,
            title=data.title.strip(),
            owner=data.owner.strip(),
            due_date=data.due_date,
            company_tax_id=CompanyTaxId(data.company_tax_id.strip()),
            description=data.description,
            requires_document=data.requires_document,
            created_at=now,
            updated_at=now,
        )
        return self._obligations.save(obligation)
