"""FastAPI application entrypoint (H1.2 skeleton).

System endpoints (no /v1 prefix, §8): GET /health, GET /openapi.json.
Domain routers mount under /v1 (§8.1 rule 1: /v1 is frozen by P1 approval).
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.errors import ApiError, problem
from app.core.logging import configure_logging, get_logger
from app.repos import models as _models  # noqa: F401  (register all tables)
from app.routers import (
    admin,
    auth,
    channels,
    clubs,
    devices,
    discover,
    events,
    invitations,
    media,
    notifications,
    registrations,
    rooms,
)
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
    from app.core.db import dispose_engine

    await dispose_engine()
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
    # Tauri WebView origins differ by platform; the deployed web origin is
    # included for the preview. Keep the list explicit instead of "*".
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "tauri://localhost",
            "http://tauri.localhost",
            "https://tauri.localhost",
            "http://localhost:5173",
            "https://etkinlikcepte.yilmazcs.xyz",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["system"], response_model=HealthResponse)
    def health() -> HealthResponse:
        """Liveness probe; no dependency checks yet (H1.2 skeleton)."""
        return HealthResponse(version=settings.app_version)

    @app.exception_handler(ApiError)
    async def api_error_handler(request, exc: ApiError):  # type: ignore[no-untyped-def]
        """Render service errors as RFC 9457 problem details."""
        return problem(exc.status_code, exc.title, exc.detail, exc.type_)

    @app.exception_handler(Exception)
    async def unhandled_exception(request, exc: Exception):  # type: ignore[no-untyped-def]
        """Return RFC 9457 instead of leaking internals.

        Fail loudly in development via the log, gently in production
        via the response body (AGENTS.md).
        """
        log.error("unhandled", path=request.url.path, error=str(exc))
        return problem(500, "Internal Server Error", "Unexpected failure.")

    web_dir = Path(settings.web_dir) if settings.web_dir else None
    if web_dir is not None and web_dir.is_dir():
        assets = web_dir / "_app"
        if assets.is_dir():
            app.mount("/_app", StaticFiles(directory=assets), name="web-assets")

        @app.get("/{path:path}", include_in_schema=False)
        async def web_app(path: str) -> FileResponse:
            """Serve the static SPA, falling back to index.html for routes."""
            candidate = (web_dir / path).resolve()
            try:
                candidate.relative_to(web_dir.resolve())
            except ValueError:
                return FileResponse(web_dir / "index.html")
            if candidate.is_file():
                return FileResponse(candidate)
            return FileResponse(web_dir / "index.html")

    for router in (
        auth.router,
        clubs.router,
        events.router,
        invitations.router,
        registrations.router,
        channels.router,
        discover.router,
        media.router,
        devices.router,
        notifications.router,
        rooms.router,
        admin.router,
    ):
        app.include_router(router, prefix=settings.api_prefix)
    return app


app = create_app()
