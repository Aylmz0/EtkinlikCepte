"""Cleaning helpers: dates, prices, venue names (H3.1)."""

from __future__ import annotations

import re
from datetime import datetime
from zoneinfo import ZoneInfo

TR_TZ = ZoneInfo("Europe/Istanbul")
_FREE_WORDS = ("ücretsiz", "ucretsiz", "bedava", "free")
_DMY = re.compile(r"(\d{1,2})[./](\d{1,2})[./](\d{4})(?:\D+(\d{1,2}):(\d{2}))?")


def clean_date(raw: object) -> datetime | None:
    """Parse ISO or dd.mm.yyyy [HH:MM] text into a timezone-aware datetime."""
    text = str(raw or "").strip()
    if not text:
        return None
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        match = _DMY.search(text)
        if not match:
            return None
        day, month, year, hour, minute = match.groups()
        try:
            parsed = datetime(int(year), int(month), int(day), int(hour or 0), int(minute or 0))
        except ValueError:
            return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=TR_TZ)


def clean_price(raw: object) -> float | None:
    """Return a price in TRY; 0.0 for free events; None when unknown."""
    text = str(raw or "").strip().lower()
    if not text:
        return None
    if any(word in text for word in _FREE_WORDS):
        return 0.0
    match = re.search(r"\d[\d.,]*", text)
    if not match:
        return None
    number = match.group(0).rstrip(".,")
    if "." in number and "," in number:
        number = number.replace(".", "").replace(",", ".")
    elif "," in number:
        number = number.replace(",", ".")
    elif re.fullmatch(r"\d{1,3}(\.\d{3})+", number):
        number = number.replace(".", "")
    try:
        return float(number)
    except ValueError:
        return None


def normalize_text(raw: object) -> str:
    """Turkish-aware lowercase, no punctuation, single spaces (for matching)."""
    text = str(raw or "").replace("İ", "i").replace("I", "ı").lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()
