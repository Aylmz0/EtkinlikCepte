"""Pydantic schemas: the single source of the OpenAPI contract (§8).

Never hand-write OpenAPI; it is generated from these models (OpenAPI 3.1).
"""

from app.schemas.common import HealthResponse, Money, ProblemDetail
from app.schemas.realtime import ClientFrame, ServerFrame, parse_client_frame

__all__ = [
    "ClientFrame",
    "HealthResponse",
    "Money",
    "ProblemDetail",
    "ServerFrame",
    "parse_client_frame",
]
