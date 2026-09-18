#!/usr/bin/env python3
"""Audit ARIS4C004 pre-exposure observability by frozen OECD FORD domains."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

VERIFIED = {"VERIFIED_SINGLE", "VERIFIED_CLUSTER"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--ford-domains", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    args = parser.parse_args()

    candidates = {r["person_id"]: r for r in read_csv(args.candidates)}
    decisions = {r["person_id"]: r for r in read_csv(args.decisions)}
    ford = {r["person_id"]: r for r in read_csv(args.ford_domains)}

    if set(candidates) != set(decisions):
        raise SystemExit("candidate and identity-decision person_id sets differ")
    if set(candidates) != set(ford):
        raise SystemExit("candidate and FORD person_id sets differ")

    groups: dict[str, list[str]] = {}
    for pid in candidates:
        field = (ford[pid].get("ford_broad_field") or "unclassified").strip() or "unclassified"
        groups.setdefault(field, []).append(pid)

    out = []
    for field, pids in sorted(groups.items()):
        statuses = [decisions[pid].get("identity_status", "") for pid in pids]
        verified = sum(status in VERIFIED for status in statuses)
        observable = sum(truthy(decisions[pid].get("network_observable")) for pid in pids)
        no_graph = sum(status == "NO_GRAPH_RECORD" for status in statuses)
        collision = sum(status == "AMBIGUOUS_COLLISION" for status in statuses)
        identity_error = sum(status == "EXCLUDED_IDENTITY_ERROR" for status in statuses)
        provisional = sum(status.startswith("PROVISIONAL") for status in statuses)
        n = len(pids)
        out.append({
            "ford_broad_field": field,
            "candidate_n": n,
            "verified_n": verified,
            "verified_rate": verified / n if n else 0.0,
            "network_observable_n": observable,
            "network_observable_rate": observable / n if n else 0.0,
            "no_graph_n": no_graph,
            "no_graph_rate": no_graph / n if n else 0.0,
            "collision_n": collision,
            "identity_error_n": identity_error,
            "provisional_n": provisional,
        })

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = list(out[0].keys()) if out else ["ford_broad_field","candidate_n"]
    with args.output_csv.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=fields)
        w.writeheader()
        w.writerows(out)

    summary = {
        "candidate_n": len(candidates),
        "ford_fields_n": len(groups),
        "all_person_ids_joined": True,
        "provisional_n": sum(row["provisional_n"] for row in out),
        "mental_health_information_used": False,
        "interpretation": "Descriptive database/network observability by frozen FORD broad field; not a field-importance comparison.",
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
