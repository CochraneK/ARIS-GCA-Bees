#!/usr/bin/env python3
"""Synchronize the Git-resident ARIS4C 000 controller snapshot."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "papers" / "dashboard.json"
OUT = ROOT / "000" / "STATUS.md"


def ids(projects: dict[str, dict], state: str, sort_progress: bool = False) -> list[str]:
    rows = [(pid, row) for pid, row in projects.items() if row.get("activity") == state]
    if sort_progress:
        rows.sort(key=lambda x: (-int(x[1].get("progress", 0)), x[0]))
    else:
        rows.sort(key=lambda x: x[0])
    return [pid for pid, _ in rows]


def main() -> int:
    data = json.loads(DASHBOARD.read_text(encoding="utf-8"))
    projects = data.get("projects", {})
    scheduling = data.get("scheduling", {})

    finish = ids(projects, "finish")
    active = ids(projects, "active", True)
    wait = ids(projects, "wait", True)
    block = ids(projects, "block", True)

    if active:
        dispatch = f"Continue **{active[0]}** first."
        if wait:
            dispatch += f" When its Active slot becomes free, the next completion-first Wait candidate is **{wait[0]}**."
    elif wait:
        dispatch = f"No paper is currently Active. Promote **{wait[0]}** next under completion-first scheduling."
    else:
        dispatch = "No Active or Wait paper is currently available. Inspect Block dependencies or reopen a Finish paper only by explicit instruction."

    text = f"""# ARIS4C 000 · Current Portfolio Status

> Generated snapshot. Canonical live portfolio state remains `papers/dashboard.json`.

- **Controller:** ARIS4C 000
- **Scheduling:** {scheduling.get('policy', 'completion-first')}
- **Canonical state:** {scheduling.get('canonical_state', 'git')}
- **Default Active WIP:** {scheduling.get('default_active_wip', 1)}
- **Maximum Active WIP:** {scheduling.get('max_active_wip', 3)}
- **States:** Finish / Active / Wait / Block
- **Paper switch rule:** checkpoint bounded substantive work to Git before switching

## Current queue snapshot

- **Finish:** {', '.join(finish) if finish else '—'}
- **Active:** {', '.join(active) if active else '—'}
- **Wait:** {', '.join(wait) if wait else '—'}
- **Block:** {', '.join(block) if block else '—'}

## Current dispatch

{dispatch}

Recalculate from `papers/dashboard.json` after any material state change.
"""
    OUT.parent.mkdir(parents=True, exist_ok=True)
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if old == text:
        print("000 controller snapshot already current.")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print("Updated 000/STATUS.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
