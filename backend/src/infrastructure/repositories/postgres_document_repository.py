from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.document import Document
from src.infrastructure.database.models.document_model import DocumentModel


class PostgresDocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, document: Document) -> Document:
        self._session.add(_to_model(document))
        self._session.flush()
        return document

    def has_document_for_obligation(self, obligation_id: UUID) -> bool:
        model = self._session.execute(
            select(DocumentModel.id)
            .where(DocumentModel.obligation_id == obligation_id)
            .limit(1)
        ).first()
        return model is not None


def _to_model(document: Document) -> DocumentModel:
    return DocumentModel(
        id=document.id,
        obligation_id=document.obligation_id,
        filename=document.filename,
        mock_url=document.mock_url,
        created_at=document.created_at,
    )
