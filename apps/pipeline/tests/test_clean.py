"""Cleaning helper tests (R11)."""

from pipeline.clean import clean_date, clean_price, normalize_text


def test_clean_price_variants() -> None:
    assert clean_price("250 TL") == 250.0
    assert clean_price("1.250,50 ₺") == 1250.5
    assert clean_price("Ücretsiz") == 0.0
    assert clean_price("") is None
    assert clean_price("belirtilmedi") is None


def test_clean_date_variants() -> None:
    assert clean_date("2026-11-12T20:00:00+03:00").hour == 20
    parsed = clean_date("12.11.2026 20:30")
    assert (parsed.year, parsed.month, parsed.day, parsed.minute) == (2026, 11, 12, 30)
    assert parsed.tzinfo is not None
    assert clean_date("yakında") is None


def test_normalize_text_turkish() -> None:
    assert normalize_text("  KÜLTÜR  Merkezi! ") == "kültür merkezi"
    assert normalize_text("IŞIK Sahnesi") == "ışık sahnesi"
