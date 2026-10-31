"""LiveKit room token response (H2.18)."""

from pydantic import BaseModel


class RoomToken(BaseModel):
    """Connection details for a LiveKit room."""

    url: str
    token: str
    room: str
