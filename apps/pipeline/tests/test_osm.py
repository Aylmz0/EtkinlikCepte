"""OSM fixture test: grey points are produced, invalid geometry rejected (R11)."""

from pipeline.osm import parse_overpass

FIXTURE = {
    "elements": [
        {"type": "node", "id": 1, "lat": 41.0082, "lon": 28.9784,
         "tags": {"amenity": "theatre", "name": "Şehir Tiyatrosu", "wheelchair": "yes"}},
        {"type": "way", "id": 2,
         "geometry": [{"lat": 41.0, "lon": 29.0}, {"lat": 41.0, "lon": 29.001},
                      {"lat": 41.001, "lon": 29.001}, {"lat": 41.0, "lon": 29.0}],
         "tags": {"amenity": "cinema", "name": "Sinema Salonu"}},
        {"type": "way", "id": 3,  # bow-tie: self-intersecting, invalid
         "geometry": [{"lat": 41.0, "lon": 29.0}, {"lat": 41.001, "lon": 29.001},
                      {"lat": 41.001, "lon": 29.0}, {"lat": 41.0, "lon": 29.001},
                      {"lat": 41.0, "lon": 29.0}],
         "tags": {"amenity": "theatre", "name": "Bozuk Poligon"}},
        {"type": "node", "id": 4, "lat": 10.0, "lon": 10.0,
         "tags": {"amenity": "theatre", "name": "Türkiye Dışı"}},
        {"type": "node", "id": 5, "lat": 41.0, "lon": 29.0, "tags": {"amenity": "theatre"}},
        {"type": "node", "id": 6, "lat": 41.0, "lon": 29.0,
         "tags": {"shop": "bakery", "name": "Fırın"}},
    ]
}


def test_grey_points_from_fixture() -> None:
    venues, rejected = parse_overpass(FIXTURE)
    assert [v["source_ref"] for v in venues] == ["node/1", "way/2"]
    assert venues[0]["wheelchair_accessible"] is True
    assert venues[0]["category"] == "amenity=theatre"
    assert rejected == 4
