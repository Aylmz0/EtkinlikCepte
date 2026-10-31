"""Discovery response schemas (§8 Keşif, H2.6/H2.16/H2.17)."""

from __future__ import annotations

import datetime
import uuid

from pydantic import BaseModel, Field


class VenueOut(BaseModel):
    """A venue inside a map bounding box."""

    id: uuid.UUID
    name: str
    category: str | None = None
    address: str | None = None
    city: str | None = None
    lat: float
    lng: float


class VenueListResponse(BaseModel):
    """Venue result page."""

    count: int
    items: list[VenueOut]


class EventOut(BaseModel):
    """An event shown in discovery and recommendations."""

    id: uuid.UUID
    title: str
    category: str | None = None
    starts_at: datetime.datetime
    ends_at: datetime.datetime | None = None
    venue_id: uuid.UUID | None = None
    venue_name: str | None = None
    club_id: uuid.UUID | None = None
    club_name: str | None = None
    lat: float
    lng: float
    distance_m: float | None = None
    price_minor: int | None = None
    currency: str = "TRY"


class EventListResponse(BaseModel):
    """Event result page."""

    count: int
    items: list[EventOut]


class RankingWeights(BaseModel):
    """Transparent recommendation weights (loaded from ranking_weights)."""

    w1_distance: float = Field(default=0.30, ge=0)
    w2_category: float = Field(default=0.20, ge=0)
    w3_freshness: float = Field(default=0.10, ge=0)
    w4_popularity: float = Field(default=0.15, ge=0)
    w5_price: float = Field(default=0.10, ge=0)
    w6_club_follow: float = Field(default=0.15, ge=0)

    def normalized(self) -> RankingWeights:
        """Scale weights so their sum is 1; fall back to defaults when zero."""
        total = (
            self.w1_distance
            + self.w2_category
            + self.w3_freshness
            + self.w4_popularity
            + self.w5_price
            + self.w6_club_follow
        )
        if total <= 0:
            return RankingWeights()
        return RankingWeights(
            w1_distance=self.w1_distance / total,
            w2_category=self.w2_category / total,
            w3_freshness=self.w3_freshness / total,
            w4_popularity=self.w4_popularity / total,
            w5_price=self.w5_price / total,
            w6_club_follow=self.w6_club_follow / total,
        )


class ScoreFactor(BaseModel):
    """One explainable contribution to a recommendation score."""

    key: str
    label: str
    raw: float
    normalized: float
    weight: float
    contribution: float


class RecommendationOut(BaseModel):
    """An event with its score and human-readable reason."""

    event: EventOut
    score: float
    reason: str
    factors: list[ScoreFactor]


class RecommendationsResponse(BaseModel):
    """Recommendation page with the weights used."""

    count: int
    candidate_count: int
    weights: RankingWeights
    generated_at: datetime.datetime
    items: list[RecommendationOut]
