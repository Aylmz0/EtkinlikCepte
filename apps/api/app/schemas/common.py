"""Contract-wide shared shapes (§8.1)."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Money(BaseModel):
    """Money as integer minor units plus ISO-4217 currency, never float."""

    amount_minor: int = Field(ge=0, examples=[12500])
    currency: str = Field(min_length=3, max_length=3, examples=["TRY"])


class ProblemDetail(BaseModel):
    """RFC 9457 error body (§8.1 rule 5)."""

    type: str = "about:blank"
    title: str
    status: int
    detail: str


class HealthResponse(BaseModel):
    """GET /health response shape."""

    status: str = "ok"
    version: str
