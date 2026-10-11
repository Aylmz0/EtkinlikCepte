"""Admin endpoints: sources, reports, audit (§8 Yönetim/Şikâyet). Owner: P1 (+P2/P3)."""

from fastapi import APIRouter

router = APIRouter(prefix="/admin", tags=["admin"])
