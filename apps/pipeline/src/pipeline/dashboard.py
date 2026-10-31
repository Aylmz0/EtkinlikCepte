"""Dashboard v1: per-source counts, last_status, expected vs actual (H3.2)."""

from __future__ import annotations

import html
import logging
from dataclasses import dataclass
from pathlib import Path

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class SourceReport:
    source: str
    raw: int
    clean: int
    dropped: int
    expected: int
    last_status: str
    missing: int  # expected - clean, never hidden


def build_report(
    stats: dict[str, dict[str, int | str]], expected: dict[str, int]
) -> list[SourceReport]:
    """Combine load stats with expected counts; log every shortfall."""
    reports = []
    for source in sorted(set(stats) | set(expected)):
        s = stats.get(source, {})
        clean = int(s.get("clean", 0))
        want = expected.get(source, 0)
        missing = max(want - clean, 0)
        if missing:
            log.warning("missing records", extra={"source": source, "missing": missing})
        reports.append(
            SourceReport(
                source=source,
                raw=int(s.get("raw", 0)),
                clean=clean,
                dropped=int(s.get("dropped", 0)),
                expected=want,
                last_status=str(s.get("last_status", "never_ran")),
                missing=missing,
            )
        )
    return reports


def render_html(reports: list[SourceReport]) -> str:
    head = "".join(
        f"<th>{h}</th>"
        for h in ("Kaynak", "Ham", "Temiz", "Elenen", "Beklenen", "Eksik", "last_status")
    )
    rows = "".join(
        f"<tr><td>{html.escape(r.source)}</td><td>{r.raw}</td><td>{r.clean}</td>"
        f"<td>{r.dropped}</td><td>{r.expected}</td>"
        f'<td style="color:{"#b00" if r.missing else "#080"}">{r.missing}</td>'
        f"<td>{html.escape(r.last_status)}</td></tr>"
        for r in reports
    )
    return (
        '<!doctype html><meta charset="utf-8"><title>Pano v1</title>'
        f"<h1>Veri hattı panosu</h1><table border=1 cellpadding=6><tr>{head}</tr>{rows}</table>"
    )


def write_dashboard(reports: list[SourceReport], path: Path) -> Path:
    path.write_text(render_html(reports), encoding="utf-8")
    return path
