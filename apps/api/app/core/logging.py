"""structlog setup shared by the API process (§3.2)."""

from __future__ import annotations

import structlog

_configured = False


def configure_logging(level: str = "INFO") -> None:
    """Configure structlog with JSON output exactly once.

    Args:
        level: Root log level name (e.g. "INFO", "DEBUG").
    """
    global _configured
    if _configured:
        return
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(level),
        cache_logger_on_first_use=True,
    )
    _configured = True


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Return a bound structlog logger.

    Args:
        name: Logger name, usually __name__ of the caller.

    Returns:
        A structlog logger bound to the given name.
    """
    return structlog.get_logger(name)
