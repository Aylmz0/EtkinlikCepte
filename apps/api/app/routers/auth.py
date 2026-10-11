"""Auth endpoints (§8 Kimlik). Owner: P1, lands in H2.1."""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])
