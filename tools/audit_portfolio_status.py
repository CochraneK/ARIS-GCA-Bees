#!/usr/bin/env python3
"""Audit the simplified ARIS4C portfolio activity taxonomy."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "papers" / "dashboard.json"
ALLOWED = {"finish", "active", "wait", "block"}
LEGACY = {"quiet", "waiting", "gated", "blocked"}


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

    manifest_ids = {
        p.parent.name[:3]
        for p in (ROOT / "papers").glob("[0-9][0-9][0-9]-*/paper.json")
    }
    if set(values) != manifest_ids:
        missing = sorted(manifest_ids - set(values))
        extra = sorted(set(values) - manifest_ids)
        errors.append(f"dashboard/manifest ID mismatch: missing={missing}, extra={extra}")

    scheduling = dashboard.get("scheduling", {})
    if scheduling.get("policy") != "completion-first":
        errors.append("dashboard.scheduling.policy must be 'completion-first'")
    if scheduling.get("control_chat") != "000":
        errors.append("dashboard.scheduling.control_chat must be '000'")
    if scheduling.get("canonical_state") != "git":
        errors.append("dashboard.scheduling.canonical_state must be 'git'")
    if scheduling.get("default_active_wip") != 1:
        errors.append("dashboard.scheduling.default_active_wip must be 1")
    if scheduling.get("active_wip_policy") != "adaptive":
        errors.append("dashboard.scheduling.active_wip_policy must be 'adaptive'")
    soft_wip = scheduling.get("soft_active_wip_reference")
    if not isinstance(soft_wip, int) or soft_wip < 1:
        errors.append(
            "dashboard.scheduling.soft_active_wip_reference must be a positive integer"
        )
    max_wip = scheduling.get("max_active_wip")
    if max_wip is not None:
        errors.append(
            "dashboard.scheduling.max_active_wip must be null under adaptive WIP"
        )

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
        r'data-filter=["\']waiting["\']',
        r'data-filter=["\']quiet["\']',
        r'navWaitingCount',
        r'navQuietCount',
        r'navGatedCount',
        r'navBlockedCount',
        r'\bAt gate\b',
        r'\bWaiting\b',
        r'\bQuiet\b',
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
    configured_max = dashboard.get("scheduling", {}).get("max_active_wip")
    if configured_max is not None and counts["active"] > int(configured_max):
        errors.append(f"active WIP exceeds configured max: {counts['active']}")

    if errors:
        print("Portfolio status audit FAIL", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 1

    print(
        "Portfolio status audit PASS: "
        + ", ".join(f"{k}={counts[k]}" for k in ("finish", "active", "wait", "block"))
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
