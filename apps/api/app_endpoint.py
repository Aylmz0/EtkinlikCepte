from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/admin/sources", tags=["Source Configs"])

class SourceConfigUpdate(BaseModel):
    is_active: Optional[bool] = None
    schedule_cron: Optional[str] = None
    rate_limit_seconds: Optional[int] = None

@router.get("/")
def list_sources():
    """Tüm kaynak konfigürasyonlarını listeler (Veritabanı bağlantısı H2.8'de aktifleşecek)."""
    # Mock data return
    return [{"id": 1, "source_name": "ornek_kultur_sanat", "is_active": True, "schedule_cron": "0 */2 * * *"}]

@router.patch("/{source_id}")
def update_source(source_id: int, config: SourceConfigUpdate):
    """Kaynak ayarlarını günceller."""
    return {"message": f"Source {source_id} updated successfully", "updated_fields": config.dict(exclude_unset=True)}

@router.post("/{source_id}/run")
def run_source_manually(source_id: int):
    """Belirtilen kaynağı manuel tetikler (Dramatiq kuyruğuna görev atar)."""
    # Örn: fetch_rss_feed.send(source_name)
    return {"message": f"Source {source_id} triggered manually via Dramatiq."}
