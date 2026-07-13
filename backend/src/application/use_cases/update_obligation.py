from datetime import datetime, timezone
from uuid import UUID

from src.application.dtos.obligation_dto import UpdateObligationInput
from src.application.errors import ConcurrencyConflictError, NotFoundError
from src.domain.entities.obligation import Obligation
from src.domain.value_objects.company_tax_id import CompanyTaxId


class UpdateObligationUseCase:
    def __init__(self, obligation_repository) -> None:
        self._obligations = obligation_repository

    def execute(
        self,
        obligation_id: UUID,
        data: UpdateObligationInput,
        expected_version: int,
    ) -> Obligation:
        if not data.title.strip():
            raise ValueError("title is required")
        if not data.owner.strip():
            raise ValueError("owner is required")

        obligation = self._obligations.get_by_id(obligation_id)
        if obligation is None:
            raise NotFoundError("obligation", str(obligation_id))
        if obligation.version != expected_version:
            raise ConcurrencyConflictError()

        obligation.type = data.type
        obligation.title = data.title.strip()
        obligation.owner = data.owner.strip()
        obligation.due_date = data.due_date
        obligation.company_tax_id = CompanyTaxId(data.company_tax_id.strip())
        obligation.description = data.description
        obligation.requires_document = data.requires_document
        obligation.updated_at = datetime.now(timezone.utc)

        return self._obligations.update(obligation, expected_version)
