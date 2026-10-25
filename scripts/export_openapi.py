"""Write the FastAPI OpenAPI document for client generation (H2.12)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps/api"))

from app.main import app  # noqa: E402

TARGET = ROOT / "packages/api-client/openapi.json"


def main() -> None:
    """Serialize the current contract with stable formatting."""
    TARGET.write_text(json.dumps(app.openapi(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
