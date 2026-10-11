"""RFC 9457 problem-details helpers (§8.1 rule 5).

Every error response uses content type application/problem+json with a
machine-readable type and a human-readable title.
"""

from __future__ import annotations

from fastapi.responses import JSONResponse


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
