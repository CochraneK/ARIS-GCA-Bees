#!/usr/bin/env python3
"""Show the ARIS4C completion-first execution queue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DASHBOARD = ROOT / "papers" / "dashboard.json"


def load_dashboard() -> dict:
    return json.loads(DASHBOARD.read_text(encoding="utf-8"))


def wait_key(item: tuple[str, dict]) -> tuple:
    pid, row = item
    progress = int(row.get("progress", 0))
    # Deterministic baseline ordering. Human/agent judgment may override ties
    # using bounded-unit size, finishability, and execution cost.
    return (-progress, pid)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--slots",
        type=int,
        default=None,
        help=(
            "target Active execution capacity; no fixed maximum. "
            "Omit to use dashboard default_active_wip."
        ),
    )
    args = parser.parse_args()

    dashboard = load_dashboard()
    projects = dashboard.get("projects", {})
    scheduling = dashboard.get("scheduling", {})
    active = sorted(
        ((pid, row) for pid, row in projects.items() if row.get("activity") == "active"),
        key=lambda x: (-int(x[1].get("progress", 0)), x[0]),
    )
    wait = sorted(
        ((pid, row) for pid, row in projects.items() if row.get("activity") == "wait"),
        key=wait_key,
    )
    block = sorted(
        ((pid, row) for pid, row in projects.items() if row.get("activity") == "block"),
        key=lambda x: (-int(x[1].get("progress", 0)), x[0]),
    )
    finish = sorted(
        ((pid, row) for pid, row in projects.items() if row.get("activity") == "finish"),
        key=lambda x: x[0],
    )

    slots = (
        int(args.slots)
        if args.slots is not None
        else int(scheduling.get("default_active_wip", 1))
    )
    if slots < 1:
        parser.error("--slots must be >= 1")
    free_slots = max(0, slots - len(active))
    promote = wait[:free_slots]

    data = {
        "policy": "completion-first",
        "active_wip_policy": scheduling.get("active_wip_policy", "adaptive"),
        "target_active_slots": slots,
        "fixed_max_active_wip": scheduling.get("max_active_wip"),
        "active": [
            {"id": pid, "progress": row.get("progress", 0), "next_gate": row.get("next_gate", "")}
            for pid, row in active
        ],
        "next_wait_candidates": [
            {"id": pid, "progress": row.get("progress", 0), "next_gate": row.get("next_gate", "")}
            for pid, row in wait
        ],
        "recommended_promotions": [
            {"id": pid, "progress": row.get("progress", 0), "next_gate": row.get("next_gate", "")}
            for pid, row in promote
        ],
        "block": [
            {"id": pid, "progress": row.get("progress", 0), "blocker": row.get("blocker", "")}
            for pid, row in block
        ],
        "finish": [{"id": pid, "progress": row.get("progress", 0)} for pid, row in finish],
    }

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    print("ARIS4C completion-first queue")
    print(f"Target Active slots: {slots}")
    print("Active:")
    for row in data["active"]:
        print(f"  {row['id']} · {row['progress']}% · {row['next_gate']}")
    print("Wait queue:")
    for i, row in enumerate(data["next_wait_candidates"], 1):
        marker = " ← next" if row["id"] in {x["id"] for x in data["recommended_promotions"]} else ""
        print(f"  {i:02d}. {row['id']} · {row['progress']}%{marker}")
    print("Block:")
    for row in data["block"]:
        print(f"  {row['id']} · {row['progress']}% · {row['blocker']}")
    print("Finish:")
    for row in data["finish"]:
        print(f"  {row['id']} · {row['progress']}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
