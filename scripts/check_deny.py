"""Fail when a dependency from deny.txt appears in a manifest or lockfile."""

from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
# Direct manifests only: lockfiles may contain transitive packages pulled by
# an allowed dependency; the deny gate reviews what a PR declares directly.
MANIFESTS = [
    ROOT / "package.json",
    ROOT / "apps/mobile/package.json",
    ROOT / "packages/ui/package.json",
    ROOT / "apps/api/pyproject.toml",
    ROOT / "apps/pipeline/pyproject.toml",
]


def main() -> int:
    """Check every manifest for a denied dependency name."""
    denied = [
        line.strip()
        for line in (ROOT / "deny.txt").read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
    failures: list[str] = []
    for path in MANIFESTS:
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")
        for name in denied:
            if name in content:
                failures.append(f"{path.relative_to(ROOT)}: {name}")
    if failures:
        print("Denied dependencies found:", *failures, sep="\n  ")
        return 1
    print(f"deny check passed ({len(denied)} names, {len(MANIFESTS)} manifests)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
