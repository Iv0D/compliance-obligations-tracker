from datetime import datetime, timezone
from uuid import UUID, uuid4

from src.application.errors import NotFoundError
from src.domain.entities.document import Document


class AttachDocumentUseCase:
    def __init__(self, obligation_repository, document_repository) -> None:
        self._obligations = obligation_repository
        self._documents = document_repository

    def execute(
        self,
        obligation_id: UUID,
        *,
        filename: str,
        mock_url: str,
    ) -> Document:
        if not filename.strip():
            raise ValueError("filename is required")
        if not mock_url.strip():
            raise ValueError("mock_url is required")

        if self._obligations.get_by_id(obligation_id) is None:
            raise NotFoundError("obligation", str(obligation_id))

        return self._documents.save(
            Document(
                id=uuid4(),
                obligation_id=obligation_id,
                filename=filename.strip(),
                mock_url=mock_url.strip(),
                created_at=datetime.now(timezone.utc),
            )
        )
