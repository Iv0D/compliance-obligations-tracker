from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config.logging import configure_logging
from src.infrastructure.database.bootstrap import create_all
from src.infrastructure.database.session import get_engine
from src.interfaces.http.errors.http_errors import register_error_handlers
from src.interfaces.http.routes import dashboard, obligations


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    create_all(get_engine())
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Compliance Obligations Tracker",
        version="0.1.0",
        description=(
            "API para seguir obligaciones de compliance: CRUD, cambio de estado "
            "con máquina de estados, invariante doc-gated, overdue derivado y "
            "audit trail. El companyTaxId se expone siempre enmascarado."
        ),
        lifespan=lifespan,
    )
    register_error_handlers(app)
    app.include_router(obligations.router)
    app.include_router(dashboard.router)

    @app.get("/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
