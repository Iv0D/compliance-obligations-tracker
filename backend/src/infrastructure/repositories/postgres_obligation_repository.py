from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy import update as sql_update
from sqlalchemy.orm import Session

from src.application.errors import ConcurrencyConflictError
from src.domain.entities.obligation import Obligation
from src.domain.value_objects.company_tax_id import CompanyTaxId
from src.infrastructure.database.models.obligation_model import ObligationModel


class PostgresObligationRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, obligation: Obligation) -> Obligation:
        self._session.add(_to_model(obligation))
        self._session.flush()
        return obligation

    def get_by_id(self, obligation_id: UUID) -> Obligation | None:
        model = self._session.get(ObligationModel, obligation_id)
        if model is None or model.deleted_at is not None:
            return None
        return _to_domain(model)

    def list_all(self) -> list[Obligation]:
        models = (
            self._session.execute(
                select(ObligationModel).where(ObligationModel.deleted_at.is_(None))
            )
            .scalars()
            .all()
        )
        return [_to_domain(model) for model in models]

    def update(self, obligation: Obligation, expected_version: int) -> Obligation:
        result = self._session.execute(
            sql_update(ObligationModel)
            .where(
                ObligationModel.id == obligation.id,
                ObligationModel.version == expected_version,
            )
            .values(
                type=obligation.type,
                title=obligation.title,
                owner=obligation.owner,
                due_date=obligation.due_date,
                company_tax_id=obligation.company_tax_id.value,
                status=obligation.status,
                description=obligation.description,
                requires_document=obligation.requires_document,
                updated_at=obligation.updated_at,
                version=expected_version + 1,
            )
        )
        if result.rowcount == 0:
            raise ConcurrencyConflictError()
        obligation.version = expected_version + 1
        return obligation

    def soft_delete(self, obligation_id: UUID, deleted_at: datetime) -> bool:
        result = self._session.execute(
            sql_update(ObligationModel)
            .where(
                ObligationModel.id == obligation_id,
                ObligationModel.deleted_at.is_(None),
            )
            .values(deleted_at=deleted_at, company_tax_id="")
        )
        return result.rowcount > 0


def _to_model(obligation: Obligation) -> ObligationModel:
    return ObligationModel(
        id=obligation.id,
        type=obligation.type,
        title=obligation.title,
        owner=obligation.owner,
        due_date=obligation.due_date,
        company_tax_id=obligation.company_tax_id.value,
        status=obligation.status,
        description=obligation.description,
        requires_document=obligation.requires_document,
        version=obligation.version,
        created_at=obligation.created_at,
        updated_at=obligation.updated_at,
        deleted_at=obligation.deleted_at,
    )


def _to_domain(model: ObligationModel) -> Obligation:
    return Obligation(
        id=model.id,
        type=model.type,
        title=model.title,
        owner=model.owner,
        due_date=model.due_date,
        company_tax_id=CompanyTaxId(model.company_tax_id),
        status=model.status,
        description=model.description,
        requires_document=model.requires_document,
        version=model.version,
        created_at=model.created_at,
        updated_at=model.updated_at,
        deleted_at=model.deleted_at,
    )
