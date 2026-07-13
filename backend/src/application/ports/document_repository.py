from typing import Protocol
from uuid import UUID

from src.domain.entities.document import Document


class DocumentRepository(Protocol):
    def save(self, document: Document) -> Document: ...

    def has_document_for_obligation(self, obligation_id: UUID) -> bool: ...
