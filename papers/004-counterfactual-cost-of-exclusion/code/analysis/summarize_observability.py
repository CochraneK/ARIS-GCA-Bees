#!/usr/bin/env python3
"""Summarize pre-exposure identity/network observability across frame strata."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

VERIFIED = {"VERIFIED_SINGLE", "VERIFIED_CLUSTER"}
NO_GRAPH = {"NO_GRAPH_RECORD"}
COLLISION = {"AMBIGUOUS_COLLISION"}
ERROR = {"EXCLUDED_IDENTITY_ERROR"}
PROVISIONAL = {"PROVISIONAL_SINGLE", "PROVISIONAL_CLUSTER"}


def truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def group_value(row: dict[str, str], variable: str) -> str:
    if variable == "birth_cohort":
        stratum = (row.get("pilot_stratum") or "").strip()
        return stratum.split("|", 1)[0] if stratum else "<missing>"
    value = (row.get(variable) or "").strip()
    return value or "<missing>"


def summarize(candidates: list[dict[str, str]], decisions: list[dict[str, str]]) -> tuple[list[dict[str, object]], dict[str, object]]:
    by_decision = {row["person_id"]: row for row in decisions}
    variables = [
        "birth_cohort",
        "pilot_stratum",
        "region",
        "gender",
        "level2_main_occ",
        "level3_main_occ",
    ]
    grouped: dict[tuple[str, str], list[tuple[dict[str, str], dict[str, str] | None]]] = defaultdict(list)
    for candidate in candidates:
        decision = by_decision.get(candidate["person_id"])
        for variable in variables:
            grouped[(variable, group_value(candidate, variable))].append((candidate, decision))

    rows: list[dict[str, object]] = []
    for (variable, value), items in sorted(grouped.items()):
        n = len(items)
        decided = 0
        verified = 0
        network = 0
        no_graph = 0
        collision = 0
        error = 0
        provisional = 0
        for _, decision in items:
            if decision is None:
                continue
            status = (decision.get("identity_status") or "").strip()
            if status:
                decided += 1
            verified += status in VERIFIED
            network += truthy(decision.get("network_observable"))
            no_graph += status in NO_GRAPH
            collision += status in COLLISION
            error += status in ERROR
            provisional += status in PROVISIONAL
        rows.append(
            {
                "group_variable": variable,
                "group_value": value,
                "candidate_n": n,
                "decision_row_n": decided,
                "verified_n": verified,
                "verified_rate": verified / n if n else 0.0,
                "network_observable_n": network,
                "network_observable_rate": network / n if n else 0.0,
                "no_graph_n": no_graph,
                "no_graph_rate": no_graph / n if n else 0.0,
                "collision_n": collision,
                "identity_error_n": error,
                "provisional_n": provisional,
            }
        )

    all_n = len(candidates)
    statuses = [(by_decision.get(row["person_id"]) or {}).get("identity_status", "") for row in candidates]
    overall = {
        "candidate_n": all_n,
        "decision_rows_n": sum(bool(by_decision.get(row["person_id"])) for row in candidates),
        "verified_n": sum(status in VERIFIED for status in statuses),
        "verified_rate": sum(status in VERIFIED for status in statuses) / all_n if all_n else 0.0,
        "network_observable_n": sum(
            truthy((by_decision.get(row["person_id"]) or {}).get("network_observable"))
            for row in candidates
        ),
        "network_observable_rate": sum(
            truthy((by_decision.get(row["person_id"]) or {}).get("network_observable"))
            for row in candidates
        ) / all_n if all_n else 0.0,
        "provisional_n": sum(status in PROVISIONAL for status in statuses),
        "no_graph_n": sum(status in NO_GRAPH for status in statuses),
        "collision_n": sum(status in COLLISION for status in statuses),
        "identity_error_n": sum(status in ERROR for status in statuses),
        "mental_health_information_used": False,
        "note": "Descriptive observability audit only; rates are not population prevalence estimates.",
    }
    return rows, overall


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    args = parser.parse_args()

    rows, overall = summarize(read_csv(args.candidates), read_csv(args.decisions))
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else [
        "group_variable",
        "group_value",
        "candidate_n",
    ]
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    args.summary_json.write_text(json.dumps(overall, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(overall, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
