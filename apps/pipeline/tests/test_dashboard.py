"""Dashboard tests: shortfalls are reported, never hidden (R11)."""

import logging
from pathlib import Path

from pipeline.dashboard import build_report, write_dashboard


def test_missing_records_are_logged_and_shown(caplog, tmp_path: Path) -> None:
    stats = {"rss": {"raw": 30, "clean": 20, "dropped": 10, "last_status": "ok"}}
    with caplog.at_level(logging.WARNING):
        reports = build_report(stats, {"rss": 25, "html": 10})
    by_source = {r.source: r for r in reports}
    assert by_source["rss"].missing == 5
    assert by_source["html"].last_status == "never_ran"
    assert "missing records" in caplog.text
    page = write_dashboard(reports, tmp_path / "pano.html").read_text(encoding="utf-8")
    assert "Veri hattı panosu" in page
