from src.application.dtos.obligation_dto import ObligationDetail, ObligationListItem
from src.domain.entities.document import Document
from src.interfaces.http.schemas.responses import (
    AuditEventResponse,
    DocumentResponse,
    ObligationDetailResponse,
    ObligationSummaryResponse,
)


def to_summary(item: ObligationListItem) -> ObligationSummaryResponse:
    obligation = item.obligation
    return ObligationSummaryResponse(
        id=str(obligation.id),
        type=obligation.type,
        title=obligation.title,
        owner=obligation.owner,
        due_date=obligation.due_date,
        status=obligation.status,
        description=obligation.description,
        requires_document=obligation.requires_document,
        company_tax_id_masked=item.company_tax_id_masked,
        is_overdue=item.is_overdue,
        version=obligation.version,
        created_at=obligation.created_at,
        updated_at=obligation.updated_at,
    )


def to_detail(detail: ObligationDetail) -> ObligationDetailResponse:
    obligation = detail.obligation
    return ObligationDetailResponse(
        id=str(obligation.id),
        type=obligation.type,
        title=obligation.title,
        owner=obligation.owner,
        due_date=obligation.due_date,
        status=obligation.status,
        description=obligation.description,
        requires_document=obligation.requires_document,
        company_tax_id_masked=detail.company_tax_id_masked,
        is_overdue=detail.is_overdue,
        version=obligation.version,
        created_at=obligation.created_at,
        updated_at=obligation.updated_at,
        audit_events=[
            AuditEventResponse(
                from_status=event.from_status,
                to_status=event.to_status,
                changed_at=event.changed_at,
            )
            for event in detail.audit_events
        ],
        valid_transitions=detail.valid_transitions,
        can_submit=detail.can_submit,
        has_document=detail.has_document,
    )


def to_document(document: Document) -> DocumentResponse:
    return DocumentResponse(
        id=str(document.id),
        obligation_id=str(document.obligation_id),
        filename=document.filename,
        mock_url=document.mock_url,
        created_at=document.created_at,
    )
