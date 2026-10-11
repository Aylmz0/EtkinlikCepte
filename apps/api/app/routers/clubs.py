"""Club, membership, follow and post endpoints (§8 Kulüp). Owner: P2, H1.8."""

from fastapi import APIRouter

router = APIRouter(prefix="/clubs", tags=["clubs"])
