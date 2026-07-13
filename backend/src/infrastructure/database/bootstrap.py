from sqlalchemy import Engine

from src.infrastructure.database.models.audit_model import AuditEventModel
from src.infrastructure.database.models.document_model import DocumentModel
from src.infrastructure.database.models.obligation_model import ObligationModel
from src.infrastructure.database.session import Base

__all__ = ["AuditEventModel", "DocumentModel", "ObligationModel", "create_all"]


def create_all(engine: Engine) -> None:
    Base.metadata.create_all(engine)
