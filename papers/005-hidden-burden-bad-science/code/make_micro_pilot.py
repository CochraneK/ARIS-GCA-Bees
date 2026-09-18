#!/usr/bin/env python3
"""Select a balanced ARIS4C005 adjudication micro-pilot.

This micro-pilot is for protocol usability / disagreement diagnostics only.
It is deliberately balanced across signal strata and MUST NOT be used to
estimate population prevalence.

Default: 10 population-random works + 10 from each of five RW enrichment
strata = 60 works.
"""

from __future__ import annotations

import argparse
import collections
import csv
import json
import random
from pathlib import Path
from typing import Any

DEFAULT_QUOTAS = {
    "population_random": 10,
    "rw_e1s_narrow": 10,
    "rw_paper_mill": 10,
    "rw_major_error": 10,
    "rw_expression_of_concern": 10,
    "rw_process_integrity": 10,
}


def group_key(row: dict[str, str]) -> str:
    if (row.get("selected_via") or "") == "population_random":
        return "population_random"
    return (row.get("rw_enrichment_stratum") or "").strip()


def parse_quotas(items: list[str]) -> dict[str, int]:
    quotas = dict(DEFAULT_QUOTAS)
    for item in items:
        if "=" not in item:
            raise ValueError(f"Quota must be group=n, got {item!r}")
        key, raw = item.split("=", 1)
        quotas[key.strip()] = int(raw)
    return quotas


def select_micro_pilot(
    rows: list[dict[str, str]],
    quotas: dict[str, int],
    seed: int,
) -> list[dict[str, str]]:
    groups: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    for row in rows:
        groups[group_key(row)].append(row)

    rng = random.Random(seed)
    selected: list[dict[str, str]] = []
    for group, n in quotas.items():
        population = groups.get(group, [])
        if len(population) < n:
            raise ValueError(
                f"Micro-pilot quota {group}={n} exceeds available {len(population)}"
            )
        selected.extend(rng.sample(population, n))

    selected.sort(key=lambda row: (group_key(row), row["paper_id"]))
    return selected


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("seed_csv", type=Path)
    parser.add_argument("micro_csv", type=Path)
    parser.add_argument("summary_json", type=Path)
    parser.add_argument("--quota", action="append", default=[])
    parser.add_argument("--seed", type=int, default=20260918)
    args = parser.parse_args()

    with args.seed_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    quotas = parse_quotas(args.quota)
    selected = select_micro_pilot(rows, quotas, args.seed)
    write_csv(args.micro_csv, selected)

    counts = collections.Counter(group_key(row) for row in selected)
    summary: dict[str, Any] = {
        "classification": "BALANCED_ADJUDICATION_MICROPILOT_NOT_PREVALENCE_SAMPLE",
        "seed": args.seed,
        "works": len(selected),
        "quotas": quotas,
        "realized_counts": dict(counts),
        "purpose": [
            "test adjudication label usability",
            "estimate disagreement/indeterminate rates",
            "estimate review effort",
            "identify evidence-access problems",
        ],
        "forbidden_use": [
            "population prevalence estimation",
            "country/journal/person ranking",
            "detector PPV estimation without design correction",
        ],
    }
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
