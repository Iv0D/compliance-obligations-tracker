from datetime import date, timedelta

from src.application.dtos.obligation_dto import DashboardKpis, ObligationListItem
from src.domain.entities.obligation import Obligation
from src.domain.services.overdue import is_overdue
from src.domain.value_objects.status import ObligationStatus

UPCOMING_WINDOW_DAYS = 7


class ListObligationsUseCase:
    def __init__(self, obligation_repository) -> None:
        self._obligations = obligation_repository

    def execute(
        self,
        *,
        status: ObligationStatus | None = None,
        today: date | None = None,
    ) -> list[ObligationListItem]:
        today = today or date.today()
        obligations = self._obligations.list_all()

        if status is not None:
            obligations = [item for item in obligations if item.status is status]

        obligations.sort(key=lambda item: item.due_date)

        return [
            ObligationListItem(
                obligation=item,
                is_overdue=is_overdue(
                    due_date=item.due_date,
                    status=item.status,
                    today=today,
                ),
                company_tax_id_masked=item.company_tax_id.masked(),
            )
            for item in obligations
        ]

    def dashboard_kpis(self, *, today: date | None = None) -> DashboardKpis:
        today = today or date.today()
        items = self.execute(today=today)
        upcoming_limit = today + timedelta(days=UPCOMING_WINDOW_DAYS)

        by_status = {status: 0 for status in ObligationStatus}
        overdue = 0
        upcoming = 0

        for item in items:
            by_status[item.obligation.status] += 1
            if item.is_overdue:
                overdue += 1
            elif (
                today <= item.obligation.due_date <= upcoming_limit
                and item.obligation.status not in {ObligationStatus.SUBMITTED, ObligationStatus.DONE}
            ):
                upcoming += 1

        return DashboardKpis(
            total=len(items),
            by_status=by_status,
            overdue=overdue,
            upcoming=upcoming,
        )
