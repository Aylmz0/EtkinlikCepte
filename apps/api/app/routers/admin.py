"""Admin endpoints: sources, reports, audit (§8 Yönetim/Şikâyet).

The source-config routes are H1.16 drafts: the contract is frozen here, the
database-backed implementation lands with H2.8/H5.10.
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, HTTPException, status

from app.schemas.source import SourceConfigRead, SourceConfigUpdate

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/sources", response_model=list[SourceConfigRead])
def list_sources() -> list[SourceConfigRead]:
    """Return configured scraper sources (empty until the DB wiring lands)."""
    return []


@router.patch("/sources/{source_id}", response_model=SourceConfigRead)
def update_source(source_id: uuid.UUID, payload: SourceConfigUpdate) -> SourceConfigRead:
    """Update one source configuration (H1.16 draft, 501 until H2.8).

    Args:
        source_id: Source-config identifier.
        payload: Partial update; omitted fields stay unchanged.

    Raises:
        HTTPException: Always 501 in the H1.16 skeleton.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Source update is wired in H2.8.",
    )


@router.post("/sources/{source_id}/run", status_code=status.HTTP_202_ACCEPTED)
def run_source(source_id: uuid.UUID) -> dict[str, str]:
    """Queue a manual source run (H1.16 draft, worker wiring in H2.8)."""
    return {"status": "accepted", "source_id": str(source_id)}
