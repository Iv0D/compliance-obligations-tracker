from datetime import datetime, timezone
from uuid import UUID

from src.application.errors import NotFoundError


class DeleteObligationUseCase:
    def __init__(self, obligation_repository) -> None:
        self._obligations = obligation_repository

    def execute(self, obligation_id: UUID) -> None:
        deleted = self._obligations.soft_delete(
            obligation_id, datetime.now(timezone.utc)
        )
        if not deleted:
            raise NotFoundError("obligation", str(obligation_id))
