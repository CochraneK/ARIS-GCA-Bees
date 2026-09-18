#!/usr/bin/env python3
"""Probability-aware two-phase sampler for ARIS4C005 Pilot B.

This sampler deliberately combines:
1) a population-random phase, and
2) detector-enriched sampling among papers not selected in phase 1.

Every selected paper receives its total inclusion probability. This is required
before any detector-enriched adjudication set may be used for population
prevalence inference.

No detector score is treated as ground truth.
"""

from __future__ import annotations

import argparse
import csv
import random
from collections import Counter
from pathlib import Path
from typing import Iterable


def parse_binary(value: str | None) -> int | None:
    if value is None:
        return None
    v = value.strip().lower()
    if v in {"", "na", "nan", "none", "null", "missing"}:
        return None
    if v in {"1", "true", "yes", "y", "positive"}:
        return 1
    if v in {"0", "false", "no", "n", "negative"}:
        return 0
    raise ValueError(f"Not a binary/missing value: {value!r}")


def signal_profile(row: dict[str, str], detector_cols: list[str]) -> tuple[int, int]:
    values = [parse_binary(row.get(c)) for c in detector_cols]
    applicable = [v for v in values if v is not None]
    positives = sum(v == 1 for v in applicable)
    return positives, len(applicable)


def enrichment_stratum(
    row: dict[str, str],
    detector_cols: list[str],
    high_specificity_cols: set[str],
) -> str:
    hs_positive = any(parse_binary(row.get(c)) == 1 for c in high_specificity_cols)
    positives, applicable = signal_profile(row, detector_cols)
    if hs_positive:
        return "high_specificity_positive"
    if positives >= 2:
        return "multi_signal_positive"
    if positives == 1:
        return "single_signal_positive"
    if applicable > 0:
        return "signal_negative"
    return "no_applicable_detector"


def choose_without_replacement(
    rng: random.Random, indices: list[int], n: int
) -> set[int]:
    if n <= 0 or not indices:
        return set()
    if n >= len(indices):
        return set(indices)
    return set(rng.sample(indices, n))


def sample_rows(
    rows: list[dict[str, str]],
    detector_cols: list[str],
    high_specificity_cols: set[str],
    n_random: int,
    n_per_enrichment: dict[str, int],
    seed: int,
) -> list[dict[str, str]]:
    if not rows:
        return []

    rng = random.Random(seed)
    n_total = len(rows)
    n_random_eff = min(max(n_random, 0), n_total)
    p_random = n_random_eff / n_total
    random_selected = choose_without_replacement(rng, list(range(n_total)), n_random_eff)

    strata: dict[str, list[int]] = {}
    for i, row in enumerate(rows):
        if i in random_selected:
            continue
        s = enrichment_stratum(row, detector_cols, high_specificity_cols)
        strata.setdefault(s, []).append(i)

    enrichment_selected: set[int] = set()
    p_enrich_conditional: dict[int, float] = {}
    for stratum, indices in strata.items():
        requested = max(int(n_per_enrichment.get(stratum, 0)), 0)
        n_eff = min(requested, len(indices))
        p = n_eff / len(indices) if indices else 0.0
        chosen = choose_without_replacement(rng, indices, n_eff)
        enrichment_selected.update(chosen)
        for i in indices:
            p_enrich_conditional[i] = p

    selected = random_selected | enrichment_selected
    output: list[dict[str, str]] = []

    for i in sorted(selected):
        row = dict(rows[i])
        s = enrichment_stratum(row, detector_cols, high_specificity_cols)
        pe = p_enrich_conditional.get(i, 0.0)
        # Phase 2 is applied only to units not selected in phase 1.
        # Hence unconditional pi = p_r + (1-p_r)*p_e.
        pi = p_random + (1.0 - p_random) * pe
        if i in random_selected:
            selected_via = "population_random"
        else:
            selected_via = f"enrichment:{s}"
        row.update(
            {
                "aris_pilot_b_stratum": s,
                "aris_selected_via": selected_via,
                "aris_pi_random": f"{p_random:.12g}",
                "aris_pi_enrich_conditional": f"{pe:.12g}",
                "aris_inclusion_probability": f"{pi:.12g}",
                "aris_design_weight": f"{(1.0 / pi):.12g}",
                "aris_sampling_seed": str(seed),
            }
        )
        output.append(row)

    return output


def read_csv(path: Path) -> tuple[list[dict[str, str]], list[str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        return list(reader), fields


def write_csv(path: Path, rows: list[dict[str, str]], original_fields: list[str]) -> None:
    extra = [
        "aris_pilot_b_stratum",
        "aris_selected_via",
        "aris_pi_random",
        "aris_pi_enrich_conditional",
        "aris_inclusion_probability",
        "aris_design_weight",
        "aris_sampling_seed",
    ]
    fields = original_fields + [c for c in extra if c not in original_fields]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def parse_targets(items: Iterable[str]) -> dict[str, int]:
    result: dict[str, int] = {}
    for item in items:
        if "=" not in item:
            raise ValueError(f"Target must be stratum=n, got {item!r}")
        key, raw = item.split("=", 1)
        result[key.strip()] = int(raw)
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("input_csv", type=Path)
    p.add_argument("output_csv", type=Path)
    p.add_argument("--detector", action="append", default=[], dest="detectors")
    p.add_argument("--high-specificity", action="append", default=[], dest="high_specificity")
    p.add_argument("--n-random", type=int, default=500)
    p.add_argument("--target", action="append", default=[])
    p.add_argument("--seed", type=int, default=20260918)
    args = p.parse_args()

    if not args.detectors:
        raise SystemExit("At least one --detector column is required.")
    unknown_hs = set(args.high_specificity) - set(args.detectors)
    if unknown_hs:
        raise SystemExit(f"High-specificity detectors must also be --detector columns: {sorted(unknown_hs)}")

    rows, fields = read_csv(args.input_csv)
    missing = [c for c in args.detectors if c not in fields]
    if missing:
        raise SystemExit(f"Missing detector columns: {missing}")

    targets = {
        "high_specificity_positive": 250,
        "multi_signal_positive": 250,
        "single_signal_positive": 250,
        "signal_negative": 250,
        "no_applicable_detector": 0,
    }
    targets.update(parse_targets(args.target))

    sampled = sample_rows(
        rows=rows,
        detector_cols=args.detectors,
        high_specificity_cols=set(args.high_specificity),
        n_random=args.n_random,
        n_per_enrichment=targets,
        seed=args.seed,
    )
    write_csv(args.output_csv, sampled, fields)

    counts = Counter(r["aris_selected_via"] for r in sampled)
    print(f"Pilot B frame rows: {len(rows)}")
    print(f"Selected rows: {len(sampled)}")
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v}")
    print("Every selected row has an explicit inclusion probability/design weight.")
    print("Detector-enriched samples MUST NOT be analyzed as simple random samples.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
