"""OSM/Overpass fixture -> venue candidates ("gri noktalar"), shapely-validated (H3.11)."""

from __future__ import annotations

import logging
from typing import Any

from shapely.geometry import Point, Polygon

log = logging.getLogger(__name__)

VENUE_TAGS: dict[str, set[str]] = {
    "amenity": {"theatre", "cinema", "arts_centre", "community_centre", "events_venue",
                "nightclub", "conference_centre"},
    "leisure": {"stadium", "sports_centre"},
}
# Turkey bounding box (lon_min, lat_min, lon_max, lat_max)
TR_BBOX = (25.5, 35.7, 44.9, 42.2)


def _category(tags: dict[str, str]) -> str | None:
    for key, values in VENUE_TAGS.items():
        if tags.get(key) in values:
            return f"{key}={tags[key]}"
    return None


def _point(element: dict[str, Any]) -> Point | None:
    """Return the venue point of a node, way polygon or ``out center`` element."""
    if element.get("type") == "node" and "lat" in element and "lon" in element:
        return Point(element["lon"], element["lat"])
    geometry = element.get("geometry")
    if element.get("type") == "way" and geometry:
        if len(geometry) < 4:
            return None
        polygon = Polygon([(p["lon"], p["lat"]) for p in geometry])
        return polygon.centroid if polygon.is_valid else None
    center = element.get("center")
    if center:
        return Point(center["lon"], center["lat"])
    return None


def _in_bbox(point: Point) -> bool:
    lon_min, lat_min, lon_max, lat_max = TR_BBOX
    return lon_min <= point.x <= lon_max and lat_min <= point.y <= lat_max


def parse_overpass(data: dict[str, Any]) -> tuple[list[dict[str, Any]], int]:
    """Turn an Overpass JSON response into venue candidates.

    Returns:
        (candidates, rejected). Rejections are logged, never silent.
    """
    seen: set[str] = set()
    venues: list[dict[str, Any]] = []
    rejected = 0
    for element in data.get("elements", []):
        tags = element.get("tags") or {}
        ref = f"{element.get('type')}/{element.get('id')}"
        category = _category(tags)
        name = str(tags.get("name") or "").strip()
        point = _point(element)
        if not category or not name or point is None or not _in_bbox(point) or ref in seen:
            log.warning("rejecting osm element", extra={"ref": ref})
            rejected += 1
            continue
        seen.add(ref)
        venues.append(
            {
                "source": "osm",
                "source_ref": ref,
                "name": name,
                "category": category,
                "city": tags.get("addr:city"),
                "lat": point.y,
                "lon": point.x,
                "wheelchair_accessible": {"yes": True, "no": False}.get(tags.get("wheelchair")),
            }
        )
    return venues, rejected
