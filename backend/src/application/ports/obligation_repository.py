from datetime import datetime
from typing import Protocol
from uuid import UUID

from src.domain.entities.obligation import Obligation


class ObligationRepository(Protocol):
    def save(self, obligation: Obligation) -> Obligation: ...

    def get_by_id(self, obligation_id: UUID) -> Obligation | None: ...

    def list_all(self) -> list[Obligation]: ...

    def update(self, obligation: Obligation, expected_version: int) -> Obligation: ...

    def soft_delete(self, obligation_id: UUID, deleted_at: datetime) -> bool: ...
