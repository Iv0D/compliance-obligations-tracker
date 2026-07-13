from datetime import date, datetime, timezone
from uuid import uuid4

import pytest

from src.domain.entities.audit_event import AuditEvent
from src.domain.errors.domain_errors import (
    DocumentRequiredError,
    InvalidCompanyTaxIdError,
    InvalidStateTransitionError,
)
from src.domain.services.overdue import is_overdue
from src.domain.services.state_machine import ensure_can_transition
from src.domain.services.tax_id_masking import redact_tax_id
from src.domain.value_objects.company_tax_id import CompanyTaxId
from src.domain.value_objects.status import ObligationStatus as S


class TestStateMachine:
    def test_allows_valid_transition(self) -> None:
        ensure_can_transition(
            current=S.PENDING,
            target=S.IN_PROGRESS,
            requires_document=False,
            has_document=False,
        )

    def test_rejects_invalid_jump(self) -> None:
        with pytest.raises(InvalidStateTransitionError):
            ensure_can_transition(
                current=S.PENDING,
                target=S.SUBMITTED,
                requires_document=False,
                has_document=False,
            )

    def test_rejects_same_status(self) -> None:
        with pytest.raises(InvalidStateTransitionError):
            ensure_can_transition(
                current=S.IN_PROGRESS,
                target=S.IN_PROGRESS,
                requires_document=False,
                has_document=False,
            )

    def test_blocks_submitted_without_document(self) -> None:
        with pytest.raises(DocumentRequiredError):
            ensure_can_transition(
                current=S.IN_PROGRESS,
                target=S.SUBMITTED,
                requires_document=True,
                has_document=False,
            )

    def test_allows_submitted_with_document(self) -> None:
        ensure_can_transition(
            current=S.IN_PROGRESS,
            target=S.SUBMITTED,
            requires_document=True,
            has_document=True,
        )


class TestOverdue:
    def test_is_overdue_when_past_due_and_not_terminal(self) -> None:
        today = date(2026, 7, 9)
        assert is_overdue(due_date=date(2026, 7, 8), status=S.PENDING, today=today)

    def test_is_not_overdue_on_due_date(self) -> None:
        today = date(2026, 7, 9)
        assert not is_overdue(due_date=today, status=S.PENDING, today=today)

    def test_is_not_overdue_when_submitted_or_done(self) -> None:
        today = date(2026, 7, 9)
        past = date(2026, 1, 1)
        assert not is_overdue(due_date=past, status=S.SUBMITTED, today=today)
        assert not is_overdue(due_date=past, status=S.DONE, today=today)


class TestCompanyTaxId:
    def test_masks_last_four_digits(self) -> None:
        assert CompanyTaxId("123456789").masked() == "••••6789"

    def test_rejects_empty_value(self) -> None:
        with pytest.raises(InvalidCompanyTaxIdError):
            CompanyTaxId("   ")


class TestTaxIdRedaction:
    def test_redacts_raw_tax_id_from_log_message(self) -> None:
        message = "creating obligation with tax 123456789"
        assert redact_tax_id(message, "123456789") == "creating obligation with tax ••••6789"


class TestAuditEvent:
    def test_status_changed_factory(self) -> None:
        obligation_id = uuid4()
        event_id = uuid4()
        changed_at = datetime(2026, 7, 9, tzinfo=timezone.utc)

        event = AuditEvent.status_changed(
            event_id=event_id,
            obligation_id=obligation_id,
            from_status=S.IN_PROGRESS,
            to_status=S.SUBMITTED,
            changed_at=changed_at,
        )

        assert event.id == event_id
        assert event.obligation_id == obligation_id
        assert event.from_status == S.IN_PROGRESS
        assert event.to_status == S.SUBMITTED
        assert event.changed_at == changed_at
