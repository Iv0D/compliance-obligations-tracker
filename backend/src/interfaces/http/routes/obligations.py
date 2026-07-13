from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from src.application.use_cases.attach_document import AttachDocumentUseCase
from src.application.use_cases.change_status import ChangeStatusUseCase
from src.application.use_cases.create_obligation import CreateObligationUseCase
from src.application.use_cases.delete_obligation import DeleteObligationUseCase
from src.application.use_cases.get_obligation import GetObligationUseCase
from src.application.use_cases.list_obligations import ListObligationsUseCase
from src.application.use_cases.update_obligation import UpdateObligationUseCase
from src.domain.value_objects.status import ObligationStatus
from src.infrastructure.repositories.postgres_audit_repository import (
    PostgresAuditRepository,
)
from src.infrastructure.repositories.postgres_document_repository import (
    PostgresDocumentRepository,
)
from src.infrastructure.repositories.postgres_obligation_repository import (
    PostgresObligationRepository,
)
from src.interfaces.http.dependencies import get_session
from src.interfaces.http.mappers.obligation_mapper import (
    to_detail,
    to_document,
    to_summary,
)
from src.interfaces.http.schemas.requests import (
    AttachDocumentRequest,
    ChangeStatusRequest,
    CreateObligationRequest,
    UpdateObligationRequest,
)
from src.interfaces.http.schemas.responses import (
    DocumentResponse,
    ErrorResponse,
    ObligationDetailResponse,
    ObligationSummaryResponse,
)

router = APIRouter(
    prefix="/obligations",
    tags=["obligations"],
    responses={
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
)


@router.post(
    "", response_model=ObligationDetailResponse, status_code=status.HTTP_201_CREATED
)
def create_obligation(
    body: CreateObligationRequest, session: Session = Depends(get_session)
) -> ObligationDetailResponse:
    created = CreateObligationUseCase(PostgresObligationRepository(session)).execute(
        body.to_input()
    )
    detail = GetObligationUseCase(
        PostgresObligationRepository(session),
        PostgresAuditRepository(session),
        PostgresDocumentRepository(session),
    ).execute(created.id)
    return to_detail(detail)


@router.get("", response_model=list[ObligationSummaryResponse])
def list_obligations(
    session: Session = Depends(get_session),
    status_filter: ObligationStatus | None = Query(default=None, alias="status"),
) -> list[ObligationSummaryResponse]:
    items = ListObligationsUseCase(PostgresObligationRepository(session)).execute(
        status=status_filter
    )
    return [to_summary(item) for item in items]


@router.get("/{obligation_id}", response_model=ObligationDetailResponse)
def get_obligation(
    obligation_id: UUID, session: Session = Depends(get_session)
) -> ObligationDetailResponse:
    detail = GetObligationUseCase(
        PostgresObligationRepository(session),
        PostgresAuditRepository(session),
        PostgresDocumentRepository(session),
    ).execute(obligation_id)
    return to_detail(detail)


@router.put("/{obligation_id}", response_model=ObligationDetailResponse)
def update_obligation(
    obligation_id: UUID,
    body: UpdateObligationRequest,
    session: Session = Depends(get_session),
) -> ObligationDetailResponse:
    UpdateObligationUseCase(PostgresObligationRepository(session)).execute(
        obligation_id, body.to_input(), expected_version=body.version
    )
    detail = GetObligationUseCase(
        PostgresObligationRepository(session),
        PostgresAuditRepository(session),
        PostgresDocumentRepository(session),
    ).execute(obligation_id)
    return to_detail(detail)


@router.delete("/{obligation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_obligation(
    obligation_id: UUID, session: Session = Depends(get_session)
) -> None:
    DeleteObligationUseCase(PostgresObligationRepository(session)).execute(obligation_id)


@router.patch("/{obligation_id}/status", response_model=ObligationDetailResponse)
def change_status(
    obligation_id: UUID,
    body: ChangeStatusRequest,
    session: Session = Depends(get_session),
) -> ObligationDetailResponse:
    ChangeStatusUseCase(
        PostgresObligationRepository(session),
        PostgresAuditRepository(session),
        PostgresDocumentRepository(session),
    ).execute(obligation_id, body.status, expected_version=body.version)
    detail = GetObligationUseCase(
        PostgresObligationRepository(session),
        PostgresAuditRepository(session),
        PostgresDocumentRepository(session),
    ).execute(obligation_id)
    return to_detail(detail)


@router.post(
    "/{obligation_id}/documents",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def attach_document(
    obligation_id: UUID,
    body: AttachDocumentRequest,
    session: Session = Depends(get_session),
) -> DocumentResponse:
    document = AttachDocumentUseCase(
        PostgresObligationRepository(session),
        PostgresDocumentRepository(session),
    ).execute(obligation_id, filename=body.filename, mock_url=body.mock_url)
    return to_document(document)
