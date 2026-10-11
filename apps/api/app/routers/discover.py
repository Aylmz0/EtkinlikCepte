"""Discovery endpoints: venues, events, recommendations (§8 Keşif). Owner: P4, H2."""

from fastapi import APIRouter

router = APIRouter(prefix="/discover", tags=["discover"])
