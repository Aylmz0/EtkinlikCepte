"""RFC 9457 problem-details helpers and the API error type (§8.1 rule 5)."""

from __future__ import annotations

from http import HTTPStatus

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException


def problem(status: int, title: str, detail: str, type_: str = "about:blank") -> JSONResponse:
    """Build an RFC 9457 error response.

    Args:
        status: HTTP status code, also stored in the body.
        title: Short human-readable summary.
        detail: Specific explanation for this occurrence.
        type_: Machine-readable problem type URI.

    Returns:
        A JSONResponse with content type application/problem+json.
    """
    return JSONResponse(
        status_code=status,
        content={"type": type_, "title": title, "status": status, "detail": detail},
        media_type="application/problem+json",
    )


class ApiError(Exception):
    """Carries an RFC 9457 problem through the service layer."""

    def __init__(
        self, status_code: int, title: str, detail: str, type_: str = "about:blank"
    ) -> None:
        self.status_code = status_code
        self.title = title
        self.detail = detail
        self.type_ = type_
        super().__init__(detail)


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Render FastAPI validation failures as RFC 9457 problem details."""
    detail = "; ".join(
        f"{'.'.join(str(part) for part in error['loc'])}: {error['msg']}" for error in exc.errors()
    )
    return problem(422, "Unprocessable Entity", detail or "Request validation failed.")


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Render Starlette/FastAPI HTTP errors as RFC 9457 problem details."""
    title = HTTPStatus(exc.status_code).phrase
    return problem(exc.status_code, title, str(exc.detail))
