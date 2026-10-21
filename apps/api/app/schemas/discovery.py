"""EtkinlikCepte – Keşif & Öneri servisi.

Bu dosya iki şeyi barındırır:
  1) `ranking_weights` tablosunun SQLAlchemy 2.0 Core tanımı
  2) Endpoint'lerin kullandığı Pydantic (v2) yanıt şemaları
"""
from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    MetaData,
    String,
    Table,
    func,
    text,
)

# ---------------------------------------------------------------------------
# 1) MODEL: ranking_weights (SQLAlchemy Core)
# ---------------------------------------------------------------------------
# Projenizde zaten ortak bir MetaData varsa, aşağıdaki satırı silip onu import edin.
metadata = MetaData()

ranking_weights = Table(
    "ranking_weights",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(64), nullable=False, unique=True),
    Column("w1_distance", Float, nullable=False, server_default=text("0.30")),
    Column("w2_category", Float, nullable=False, server_default=text("0.20")),
    Column("w3_freshness", Float, nullable=False, server_default=text("0.10")),
    Column("w4_popularity", Float, nullable=False, server_default=text("0.15")),
    Column("w5_price", Float, nullable=False, server_default=text("0.10")),
    Column("w6_club_follow", Float, nullable=False, server_default=text("0.15")),
    Column("is_active", Boolean, nullable=False, server_default=text("false")),
    Column(
        "updated_at",
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    ),
    CheckConstraint(
        "w1_distance >= 0 AND w2_category >= 0 AND w3_freshness >= 0 "
        "AND w4_popularity >= 0 AND w5_price >= 0 AND w6_club_follow >= 0",
        name="ck_ranking_weights_non_negative",
    ),
    CheckConstraint(
        "(w1_distance + w2_category + w3_freshness + w4_popularity "
        "+ w5_price + w6_club_follow) > 0",
        name="ck_ranking_weights_positive_sum",
    ),
    # Aynı anda yalnızca tek bir satır aktif olabilir.
    Index(
        "uq_ranking_weights_single_active",
        "is_active",
        unique=True,
        postgresql_where=text("is_active"),
    ),
)

# İlk kurulumda çalıştırılacak varsayılan ağırlık satırı (migration'a eklenebilir).
RANKING_WEIGHTS_SEED_SQL = """
INSERT INTO ranking_weights
    (name, w1_distance, w2_category, w3_freshness, w4_popularity, w5_price, w6_club_follow, is_active)
VALUES
    ('default', 0.30, 0.20, 0.10, 0.15, 0.10, 0.15, true)
ON CONFLICT (name) DO NOTHING;
"""


# ---------------------------------------------------------------------------
# 2) PYDANTIC ŞEMALARI
# ---------------------------------------------------------------------------
class RankingWeights(BaseModel):
    """Puanlamada kullanılan ağırlıklar (w1..w6)."""

    model_config = ConfigDict(from_attributes=True)

    w1_distance: float = Field(0.30, ge=0, description="w1 – mesafe")
    w2_category: float = Field(0.20, ge=0, description="w2 – kategori uyumu")
    w3_freshness: float = Field(0.10, ge=0, description="w3 – tazelik")
    w4_popularity: float = Field(0.15, ge=0, description="w4 – popülerlik")
    w5_price: float = Field(0.10, ge=0, description="w5 – fiyat")
    w6_club_follow: float = Field(0.15, ge=0, description="w6 – kulüp takibi")

    @property
    def total(self) -> float:
        return (
            self.w1_distance
            + self.w2_category
            + self.w3_freshness
            + self.w4_popularity
            + self.w5_price
            + self.w6_club_follow
        )

    def normalized(self) -> "RankingWeights":
        """Ağırlıkların toplamı 1 olacak şekilde ölçekler."""
        t = self.total or 1.0
        return RankingWeights(
            w1_distance=self.w1_distance / t,
            w2_category=self.w2_category / t,
            w3_freshness=self.w3_freshness / t,
            w4_popularity=self.w4_popularity / t,
            w5_price=self.w5_price / t,
            w6_club_follow=self.w6_club_follow / t,
        )


class VenueOut(BaseModel):
    id: int
    name: str
    category: str
    address: str | None = None
    lat: float
    lng: float


class VenueListResponse(BaseModel):
    count: int
    items: list[VenueOut]


class EventOut(BaseModel):
    id: int
    title: str
    category: str
    starts_at: datetime
    ends_at: datetime | None = None
    price: float = Field(description="TL cinsinden; 0 = ücretsiz")
    is_free: bool
    popularity: int = 0
    venue_id: int
    venue_name: str
    club_id: int | None = None
    club_name: str | None = None
    lat: float
    lng: float
    distance_m: float | None = Field(None, description="Kullanıcıya olan mesafe (metre)")


class EventListResponse(BaseModel):
    count: int
    items: list[EventOut]


FactorKey = Literal["distance", "category", "freshness", "popularity", "price", "club_follow"]


class ScoreFactor(BaseModel):
    """Puanın şeffaf dökümü: her faktör toplam puana ne kadar katkı yaptı."""

    key: FactorKey
    label: str = Field(description="Kullanıcıya gösterilebilir Türkçe faktör adı")
    raw: float | None = Field(None, description="Ham değer (ör. metre, gün, kişi sayısı, TL)")
    normalized: float = Field(ge=0, le=1, description="0–1 arası normalize skor")
    weight: float = Field(ge=0, description="Normalize edilmiş ağırlık (toplam = 1)")
    contribution: float = Field(ge=0, le=100, description="Toplam 100 üzerinden katkı puanı")


class RecommendationOut(BaseModel):
    event: EventOut
    score: float = Field(ge=0, le=100)
    reason: str = Field(description="'Bunu önerdik çünkü ...' formatında gerekçe")
    factors: list[ScoreFactor]


class RecommendationsResponse(BaseModel):
    count: int
    candidate_count: int = Field(description="Puanlanan kaba filtre aday sayısı (en fazla 200)")
    weights: RankingWeights = Field(description="Kullanılan normalize ağırlıklar")
    generated_at: datetime
    items: list[RecommendationOut]
