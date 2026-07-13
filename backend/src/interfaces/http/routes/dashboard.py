from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.application.use_cases.list_obligations import ListObligationsUseCase
from src.infrastructure.repositories.postgres_obligation_repository import (
    PostgresObligationRepository,
)
from src.interfaces.http.dependencies import get_session
from src.interfaces.http.schemas.responses import DashboardResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("", response_model=DashboardResponse)
def get_dashboard(session: Session = Depends(get_session)) -> DashboardResponse:
    kpis = ListObligationsUseCase(
        PostgresObligationRepository(session)
    ).dashboard_kpis()
    return DashboardResponse(
        total=kpis.total,
        by_status=kpis.by_status,
        overdue=kpis.overdue,
        upcoming=kpis.upcoming,
    )
