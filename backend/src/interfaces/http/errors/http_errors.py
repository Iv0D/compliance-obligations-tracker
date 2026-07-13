from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.application.errors import ConcurrencyConflictError, NotFoundError
from src.domain.errors.domain_errors import (
    DocumentRequiredError,
    InvalidCompanyTaxIdError,
    InvalidStateTransitionError,
)

_ERROR_MAP: dict[type[Exception], tuple[int, str]] = {
    NotFoundError: (404, "not_found"),
    ConcurrencyConflictError: (409, "conflict"),
    InvalidStateTransitionError: (422, "invalid_transition"),
    DocumentRequiredError: (422, "document_required"),
    InvalidCompanyTaxIdError: (422, "invalid_company_tax_id"),
    ValueError: (422, "validation_error"),
}


def _error_response(status_code: int, code: str, message: str) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": code, "message": message}},
    )


def register_error_handlers(app: FastAPI) -> None:
    for exc_type, (status_code, code) in _ERROR_MAP.items():

        def make_handler(status_code: int, code: str):
            async def handler(_: Request, exc: Exception) -> JSONResponse:
                return _error_response(status_code, code, str(exc))

            return handler

        app.add_exception_handler(exc_type, make_handler(status_code, code))

    async def validation_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return _error_response(422, "validation_error", str(exc.errors()))

    app.add_exception_handler(RequestValidationError, validation_handler)
