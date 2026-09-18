#!/usr/bin/env python3
"""ARIS4C007 Pilot 2: observed-only homologous-event benchmark.

Uses Januel et al. (2026) Table S1 without Amelia imputation or fitted event-scale
predictions. The benchmark asks whether life-history mappings A1/A3 predict the
human timing of *independently observed homologous events*.

Table S1 ages are post-conception days (PCD). A1/A3 operate on chronological
age after birth, so:
    chronological_years = PCD / 365.25 - gestation_years

Primary error is absolute log10 error in post-conception time, because the event
data span prenatal development through old age. This avoids letting late-life
events dominate simply because they are measured in years rather than days.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import random
import re
import statistics
import unicodedata
from collections import defaultdict
from pathlib import Path

from age_mappings import map_by_loglinear, map_by_relative_age
from build_pilot1_demography import load_pilot0_species


DAYS_PER_YEAR = 365.25

TABLE_TO_ANAGE = {
    "Felis": "Felis catus",
    "Mus musculus": "Mus musculus",
    "Pan troglodytes": "Pan troglodytes",
    "Homo sapiens": "Homo sapiens",
}

DIRECT_INPUT_PATTERNS = [
    re.compile(r"sexual\s+matur", re.I),
    re.compile(r"gestation", re.I),
    re.compile(r"maximum\s+(?:life\s*span|lifespan|longevity)", re.I),
    re.compile(r"max(?:imum)?\s+(?:life\s*span|lifespan|longevity)", re.I),
]

# Birth is the endpoint of gestation, an A1/A3 input. Match birth as a standalone
# biological event but do not exclude phrases such as "birth weight reaches...".
BIRTH_PATTERNS = [
    re.compile(r"^\s*birth\s*$", re.I),
    re.compile(r"\btime\s+of\s+birth\b", re.I),
]


def clean_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    return "".join(
        ch for ch in value.strip()
        if unicodedata.category(ch) not in {"Cf", "Cc"} or ch in "\t\n"
    ).strip()


def is_direct_input_event(timepoint: str) -> bool:
    text = clean_text(timepoint)
    return any(p.search(text) for p in DIRECT_INPUT_PATTERNS + BIRTH_PATTERNS)


def q(values: list[float], p: float) -> float:
    xs = sorted(values)
    if not xs:
        return math.nan
    if len(xs) == 1:
        return xs[0]
    pos = (len(xs) - 1) * p
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1 - frac) + xs[hi] * frac


def median(values: list[float]) -> float:
    return statistics.median(values)


def bootstrap_paired_median_difference(
    a1: list[float],
    a3: list[float],
    *,
    seed: int,
    reps: int = 10000,
) -> dict[str, object]:
    """Bootstrap median error(A3) - median error(A1), resampling event rows."""
    if len(a1) != len(a3):
        raise ValueError("paired error vectors must have equal length")
    rng = random.Random(seed)
    n = len(a1)
    diffs = []
    for _ in range(reps):
        idx = [rng.randrange(n) for _ in range(n)]
        diffs.append(
            median([a3[i] for i in idx]) - median([a1[i] for i in idx])
        )
    diffs.sort()
    return {
        "observed_median_error_difference_A3_minus_A1": median(a3) - median(a1),
        "bootstrap_reps": reps,
        "bootstrap_95pct_interval": [q(diffs, 0.025), q(diffs, 0.975)],
    }


def read_table(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    expected = {
        "Timepoint", "Environment", "PCD", "Species",
        "Statistics", "Sex", "Reference",
    }
    if not rows or not expected.issubset(rows[0]):
        raise RuntimeError(f"Unexpected Table S1 columns: {list(rows[0]) if rows else []}")
    return rows


def aggregate_events(rows: list[dict[str, str]]) -> dict[tuple[str, str, str], dict[str, float]]:
    """Replicate authors' mean-PCD aggregation by timepoint/statistics/sex/species."""
    buckets: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)

    for row in rows:
        species = clean_text(row["Species"])
        if species not in TABLE_TO_ANAGE:
            continue
        timepoint = clean_text(row["Timepoint"])
        statistics_code = clean_text(row["Statistics"])
        sex = clean_text(row["Sex"])
        try:
            pcd = float(row["PCD"])
        except (TypeError, ValueError):
            continue
        if not math.isfinite(pcd) or pcd <= 0:
            continue
        buckets[(timepoint, statistics_code, sex, species)].append(pcd)

    pivot: dict[tuple[str, str, str], dict[str, float]] = defaultdict(dict)
    for (timepoint, stats, sex, species), values in buckets.items():
        pivot[(timepoint, stats, sex)][species] = statistics.fmean(values)
    return pivot


def human_phase(observed_human_age_y: float) -> str:
    # Diagnostic bins only; they are not asserted as homologous life stages.
    if observed_human_age_y < 0:
        return "prenatal"
    if observed_human_age_y < 2:
        return "postnatal_0_2"
    if observed_human_age_y < 18:
        return "juvenile_2_18"
    if observed_human_age_y < 60:
        return "adult_18_60"
    return "late_60_plus"


def metrics(errors_log10: list[float], abs_year_errors: list[float]) -> dict[str, float]:
    return {
        "n_events": len(errors_log10),
        "median_abs_log10_error": median(errors_log10),
        "mean_abs_log10_error": statistics.fmean(errors_log10),
        "p75_abs_log10_error": q(errors_log10, 0.75),
        "p90_abs_log10_error": q(errors_log10, 0.90),
        "median_fold_error": 10 ** median(errors_log10),
        "median_absolute_human_chronological_error_y": median(abs_year_errors),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--table-s1", type=Path, required=True)
    ap.add_argument("--pilot0-grid", type=Path, required=True)
    ap.add_argument("--pilot0-coverage", type=Path, required=True)
    ap.add_argument("--out", type=Path, default=Path("data/pilot2_events"))
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    species_times, upstream = load_pilot0_species(
        args.pilot0_grid, args.pilot0_coverage
    )
    human = species_times["Homo sapiens"]

    raw = read_table(args.table_s1)
    pivot = aggregate_events(raw)

    output: list[dict[str, object]] = []
    source_labels = ["Felis", "Mus musculus", "Pan troglodytes"]

    for key, ages in sorted(pivot.items()):
        timepoint, stats, sex = key
        if "Homo sapiens" not in ages:
            continue

        human_pcd_days = ages["Homo sapiens"]
        observed_human_age_y = human_pcd_days / DAYS_PER_YEAR - human.gestation_y
        direct_input = is_direct_input_event(timepoint)

        for source_label in source_labels:
            if source_label not in ages:
                continue

            anage_name = TABLE_TO_ANAGE[source_label]
            source = species_times.get(anage_name)
            if source is None:
                continue

            source_pcd_days = ages[source_label]
            source_age_y = source_pcd_days / DAYS_PER_YEAR - source.gestation_y

            for method, mapper in (
                ("A1_relative_lifespan", map_by_relative_age),
                ("A3_loglinear", map_by_loglinear),
            ):
                try:
                    predicted_human_age_y = mapper(source_age_y, source, human)
                    predicted_human_pcd_y = predicted_human_age_y + human.gestation_y
                except (ValueError, OverflowError):
                    continue

                observed_human_pcd_y = human_pcd_days / DAYS_PER_YEAR
                if predicted_human_pcd_y <= 0 or observed_human_pcd_y <= 0:
                    continue

                abs_log_error = abs(
                    math.log10(predicted_human_pcd_y)
                    - math.log10(observed_human_pcd_y)
                )

                output.append(
                    {
                        "source_species_label": source_label,
                        "source_species_anage": anage_name,
                        "timepoint": timepoint,
                        "statistics": stats,
                        "sex": sex,
                        "source_pcd_days": source_pcd_days,
                        "observed_human_pcd_days": human_pcd_days,
                        "source_chronological_age_y": source_age_y,
                        "observed_human_chronological_age_y": observed_human_age_y,
                        "human_phase": human_phase(observed_human_age_y),
                        "direct_mapping_input_overlap": int(direct_input),
                        "strict_heldout": int(not direct_input),
                        "method": method,
                        "predicted_human_chronological_age_y": predicted_human_age_y,
                        "predicted_human_pcd_y": predicted_human_pcd_y,
                        "absolute_log10_pcd_error": abs_log_error,
                        "fold_error": 10 ** abs_log_error,
                        "absolute_human_chronological_error_y": abs(
                            predicted_human_age_y - observed_human_age_y
                        ),
                    }
                )

    if not output:
        raise RuntimeError("No paired observed human/source events were generated")

    out_csv = args.out / "observed_event_predictions.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(output[0]))
        writer.writeheader()
        writer.writerows(output)

    # Collapse method rows into paired errors for each event.
    pair_key_fields = (
        "source_species_label", "timepoint", "statistics", "sex",
    )
    pairs: dict[tuple[str, ...], dict[str, dict[str, object]]] = defaultdict(dict)
    for row in output:
        key = tuple(str(row[f]) for f in pair_key_fields)
        pairs[key][str(row["method"])] = row

    paired = [
        methods for methods in pairs.values()
        if {"A1_relative_lifespan", "A3_loglinear"}.issubset(methods)
    ]

    def summarize_subset(
        name: str,
        predicate,
        *,
        seed: int,
    ) -> dict[str, object]:
        selected = [
            p for p in paired
            if predicate(p["A1_relative_lifespan"])
        ]
        a1_log = [
            float(p["A1_relative_lifespan"]["absolute_log10_pcd_error"])
            for p in selected
        ]
        a3_log = [
            float(p["A3_loglinear"]["absolute_log10_pcd_error"])
            for p in selected
        ]
        a1_year = [
            float(p["A1_relative_lifespan"]["absolute_human_chronological_error_y"])
            for p in selected
        ]
        a3_year = [
            float(p["A3_loglinear"]["absolute_human_chronological_error_y"])
            for p in selected
        ]
        if not selected:
            return {"n_events": 0}

        return {
            "n_events": len(selected),
            "A1_relative_lifespan": metrics(a1_log, a1_year),
            "A3_loglinear": metrics(a3_log, a3_year),
            "paired_bootstrap_median_log_error_difference":
                bootstrap_paired_median_difference(
                    a1_log, a3_log, seed=seed
                ),
        }

    subsets = {
        "all_observed_pairs": summarize_subset(
            "all_observed_pairs", lambda r: True, seed=202609180
        ),
        "strict_heldout": summarize_subset(
            "strict_heldout",
            lambda r: int(r["strict_heldout"]) == 1,
            seed=202609181,
        ),
    }

    for i, source_label in enumerate(source_labels, start=2):
        subsets[f"strict_heldout__{source_label}"] = summarize_subset(
            f"strict_heldout__{source_label}",
            lambda r, s=source_label: (
                int(r["strict_heldout"]) == 1
                and r["source_species_label"] == s
            ),
            seed=202609180 + i,
        )

    phases = [
        "prenatal", "postnatal_0_2", "juvenile_2_18",
        "adult_18_60", "late_60_plus",
    ]
    for i, phase in enumerate(phases, start=10):
        subsets[f"strict_heldout_phase__{phase}"] = summarize_subset(
            f"strict_heldout_phase__{phase}",
            lambda r, ph=phase: (
                int(r["strict_heldout"]) == 1 and r["human_phase"] == ph
            ),
            seed=202609180 + i,
        )

    # Audit exact events excluded as direct overlap.
    excluded_keys = sorted({
        (str(r["timepoint"]), str(r["statistics"]), str(r["sex"]))
        for r in output if int(r["direct_mapping_input_overlap"]) == 1
    })

    summary = {
        "source_table_rows": len(raw),
        "aggregated_event_keys": len(pivot),
        "paired_event_keys_with_both_methods": len(paired),
        "strict_heldout_pair_keys": sum(
            1 for p in paired
            if int(p["A1_relative_lifespan"]["strict_heldout"]) == 1
        ),
        "species_mapping": TABLE_TO_ANAGE,
        "upstream_life_history": upstream,
        "primary_metric": (
            "absolute log10 error in post-conception time; "
            "median fold error = 10^median_abs_log10_error"
        ),
        "strict_heldout_rule": {
            "excluded_direct_input_patterns": [
                "sexual maturity",
                "gestation",
                "maximum lifespan/longevity",
                "standalone/time-of-birth",
            ],
            "excluded_unique_event_keys": [
                {"timepoint": x[0], "statistics": x[1], "sex": x[2]}
                for x in excluded_keys
            ],
        },
        "subsets": subsets,
        "guardrails": [
            "No Amelia imputation is used in this observed-only benchmark.",
            "No Januel event-scale model is trained or evaluated here.",
            "A1/A3 are evaluated only against paired empirical event timings.",
            "Primary log-time error handles the prenatal-to-late-life dynamic range.",
            "Human phase bins are diagnostic labels, not claims of homologous stages.",
            "Repeated observations are averaged using the Januel grouping key: timepoint × statistics × sex × species.",
        ],
    }

    (args.out / "observed_event_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
