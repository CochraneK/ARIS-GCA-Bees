#!/usr/bin/env python3
"""Audit the simplified ARIS4C portfolio activity taxonomy."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "papers" / "dashboard.json"
ALLOWED = {"active", "waiting", "quiet"}
LEGACY = {"gated", "blocked"}


def main() -> int:
    errors: list[str] = []
    dashboard = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    projects = dashboard.get("projects", {})

    values = {}
    for pid, row in sorted(projects.items()):
        activity = str(row.get("activity", "")).lower()
        values[pid] = activity
        if activity not in ALLOWED:
            errors.append(f"{pid}: invalid activity={activity!r}; allowed={sorted(ALLOWED)}")

    if len(values) != 16:
        errors.append(f"expected 16 dashboard projects, found {len(values)}")

    # Generated public surfaces must not reintroduce the legacy activity taxonomy.
    checks = [
        ROOT / "README.md",
        ROOT / "README.en.md",
        ROOT / "docs" / "index.html",
        ROOT / "docs" / "command-center.js",
    ]
    legacy_patterns = [
        r'data-filter=["\']gated["\']',
        r'data-filter=["\']blocked["\']',
        r'navGatedCount',
        r'navBlockedCount',
        r'\bAt gate\b',
    ]
    for path in checks:
        if not path.exists():
            errors.append(f"missing public/status surface: {path.relative_to(ROOT)}")
            continue
        text = path.read_text(encoding="utf-8")
        for pattern in legacy_patterns:
            if re.search(pattern, text):
                errors.append(f"{path.relative_to(ROOT)}: legacy activity surface matched {pattern}")

    counts = {state: sum(v == state for v in values.values()) for state in sorted(ALLOWED)}
    if sum(counts.values()) != len(values):
        errors.append("activity states are not MECE")

    if errors:
        print("Portfolio status audit FAIL", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 1

    print(
        "Portfolio status audit PASS: "
        + ", ".join(f"{k}={counts[k]}" for k in ("active", "waiting", "quiet"))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
