#!/usr/bin/env python3
"""Rebuild ARIS4C portfolio progress history from Git snapshots of papers/dashboard.json."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_PATH = "papers/dashboard.json"
OUT = ROOT / "papers" / "progress_history.json"


def run_git(*args: str) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return proc.stdout


def load_dashboard_at(ref: str) -> dict | None:
    try:
        raw = run_git("show", f"{ref}:{DASHBOARD_PATH}")
    except subprocess.CalledProcessError:
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


def main() -> int:
    log = run_git("log", "--reverse", "--format=%H%x09%cI", "--", DASHBOARD_PATH)
    points = []
    last_signature = None

    for line in log.splitlines():
        if not line.strip():
            continue
        sha, ts = line.split("\t", 1)
        data = load_dashboard_at(sha)
        if not data:
            continue
        projects = data.get("projects", {})
        progress = {
            str(pid): int(row.get("progress", 0) or 0)
            for pid, row in sorted(projects.items())
        }
        activity = {
            str(pid): str(row.get("activity", "") or "")
            for pid, row in sorted(projects.items())
        }
        if not progress:
            continue
        mean_progress = round(sum(progress.values()) / len(progress), 2)
        finish_count = sum(1 for state in activity.values() if state in {"finish", "quiet"})
        signature = (tuple(progress.items()), tuple(activity.items()))
        if signature == last_signature:
            continue
        last_signature = signature
        points.append({
            "commit": sha[:12],
            "timestamp": ts,
            "tracked": len(progress),
            "mean_progress": mean_progress,
            "finish_count": finish_count,
            "projects": progress,
        })

    payload = {
        "schema_version": 1,
        "source": "git history of papers/dashboard.json",
        "points": points,
    }
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
    if old == text:
        print(f"Progress history already current: {len(points)} checkpoints")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"Rebuilt progress history: {len(points)} checkpoints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
