from datetime import date, datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.application.errors import ConcurrencyConflictError
from src.domain.entities.obligation import Obligation
from src.domain.value_objects.company_tax_id import CompanyTaxId
from src.domain.value_objects.obligation_type import ObligationType
from src.domain.value_objects.status import ObligationStatus
from src.infrastructure.database.bootstrap import create_all
from src.infrastructure.repositories.postgres_obligation_repository import (
    PostgresObligationRepository,
)


@pytest.fixture
def session_factory():
    engine = create_engine("sqlite://", future=True)
    create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)


def _make_obligation() -> Obligation:
    now = datetime(2026, 7, 9, tzinfo=timezone.utc)
    return Obligation(
        id=uuid4(),
        type=ObligationType.ANNUAL_REPORT,
        title="Annual report",
        owner="Ana",
        due_date=date(2026, 12, 1),
        company_tax_id=CompanyTaxId("123456789"),
        created_at=now,
        updated_at=now,
    )


def test_save_and_get_roundtrip(session_factory) -> None:
    obligation = _make_obligation()
    with session_factory() as session:
        PostgresObligationRepository(session).save(obligation)
        session.commit()

    with session_factory() as session:
        loaded = PostgresObligationRepository(session).get_by_id(obligation.id)

    assert loaded is not None
    assert loaded.id == obligation.id
    assert loaded.company_tax_id.masked() == "••••6789"
    assert loaded.status is ObligationStatus.PENDING
    assert loaded.version == 1


def test_update_increments_version(session_factory) -> None:
    obligation = _make_obligation()
    with session_factory() as session:
        PostgresObligationRepository(session).save(obligation)
        session.commit()

    with session_factory() as session:
        repo = PostgresObligationRepository(session)
        obligation.status = ObligationStatus.IN_PROGRESS
        updated = repo.update(obligation, expected_version=1)
        session.commit()

    assert updated.version == 2


def test_optimistic_lock_rejects_stale_version(session_factory) -> None:
    obligation = _make_obligation()
    with session_factory() as session:
        PostgresObligationRepository(session).save(obligation)
        session.commit()

    # First writer wins, bumping version 1 -> 2.
    with session_factory() as session:
        repo = PostgresObligationRepository(session)
        obligation.status = ObligationStatus.IN_PROGRESS
        repo.update(obligation, expected_version=1)
        session.commit()

    # Second writer still holds version 1 and must be rejected.
    with session_factory() as session:
        repo = PostgresObligationRepository(session)
        with pytest.raises(ConcurrencyConflictError):
            repo.update(obligation, expected_version=1)
