from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.domain.entities.audit_event import AuditEvent
from src.infrastructure.database.models.audit_model import AuditEventModel


class PostgresAuditRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, event: AuditEvent) -> AuditEvent:
        self._session.add(_to_model(event))
        self._session.flush()
        return event

    def list_by_obligation_id(self, obligation_id: UUID) -> list[AuditEvent]:
        models = (
            self._session.execute(
                select(AuditEventModel)
                .where(AuditEventModel.obligation_id == obligation_id)
                .order_by(AuditEventModel.changed_at)
            )
            .scalars()
            .all()
        )
        return [_to_domain(model) for model in models]


def _to_model(event: AuditEvent) -> AuditEventModel:
    return AuditEventModel(
        id=event.id,
        obligation_id=event.obligation_id,
        from_status=event.from_status,
        to_status=event.to_status,
        changed_at=event.changed_at,
    )


def _to_domain(model: AuditEventModel) -> AuditEvent:
    return AuditEvent(
        id=model.id,
        obligation_id=model.obligation_id,
        from_status=model.from_status,
        to_status=model.to_status,
        changed_at=model.changed_at,
    )
