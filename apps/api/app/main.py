"""FastAPI application entrypoint (H1.2 skeleton).

System endpoints (no /v1 prefix, §8): GET /health, GET /openapi.json.
Domain routers mount under /v1 (§8.1 rule 1: /v1 is frozen by P1 approval).
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.core.config import settings
from app.core.errors import problem
from app.core.logging import configure_logging, get_logger
from app.routers import admin, auth, channels, clubs, discover, events, media
from app.schemas import HealthResponse

log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Start up logging; pools stay lazy until H1.3/H1.4 need them.

    Args:
        app: The FastAPI application instance.

    Yields:
        Control to the running application.
    """
    configure_logging(settings.log_level)
    log.info("startup", version=settings.app_version)
    yield
    log.info("shutdown")


def create_app() -> FastAPI:
    """Build the FastAPI application with system endpoints and /v1 routers.

    Returns:
        The configured FastAPI application.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    @app.get("/health", tags=["system"], response_model=HealthResponse)
    def health() -> HealthResponse:
        """Liveness probe; no dependency checks yet (H1.2 skeleton)."""
        return HealthResponse(version=settings.app_version)

    @app.exception_handler(Exception)
    async def unhandled_exception(request, exc: Exception):  # type: ignore[no-untyped-def]
        """Return RFC 9457 instead of leaking internals.

        Fail loudly in development via the log, gently in production
        via the response body (AGENTS.md).
        """
        log.error("unhandled", path=request.url.path, error=str(exc))
        return problem(500, "Internal Server Error", "Unexpected failure.")

    for router in (
        auth.router,
        clubs.router,
        events.router,
        channels.router,
        discover.router,
        media.router,
        admin.router,
    ):
        app.include_router(router, prefix=settings.api_prefix)
    return app


app = create_app()
