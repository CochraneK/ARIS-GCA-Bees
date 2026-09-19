#!/usr/bin/env python3
"""Build a leakage-safe landmark dataset for delayed-recognition prediction.

For each mature paper, features use only citation information available through
landmark age L. Full-history delayed-recognition metrics are kept only as future
outcomes.

Primary row semantics:
- features_* : computed from ages 0..L only
- outcome_*  : computed from full history
- eligible   : requires follow-up through L + H

No natural Sleeping Beauty threshold is imposed.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

from sleeping_beauty import paper_metrics


def slope(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    xs = list(range(len(values)))
    xbar = sum(xs) / len(xs)
    ybar = sum(values) / len(values)
    denom = sum((x - xbar) ** 2 for x in xs)
    if denom == 0:
        return 0.0
    return sum((x - xbar) * (y - ybar) for x, y in zip(xs, values)) / denom


def citation_features(citations: list[int]) -> dict[str, Any]:
    if not citations:
        raise ValueError("citation feature window is empty")
    total = sum(citations)
    return {
        "feature_citations_cumulative": total,
        "feature_citations_last_year": citations[-1],
        "feature_citations_max_annual": max(citations),
        "feature_citations_mean_annual": total / len(citations),
        "feature_zero_citation_years": sum(1 for x in citations if x == 0),
        "feature_positive_citation_years": sum(1 for x in citations if x > 0),
        "feature_citation_slope": slope([float(x) for x in citations]),
    }


def build_landmark_row(
    paper_id: str,
    publication_year: int,
    counts_by_year: dict[int, int],
    *,
    landmark_age: int,
    horizon_years: int,
    observation_end_year: int,
    openalex_id: str = "",
) -> dict[str, Any]:
    if landmark_age < 0:
        raise ValueError("landmark_age must be >=0")
    if horizon_years <= 0:
        raise ValueError("horizon_years must be >0")
    if observation_end_year < publication_year:
        raise ValueError("observation_end_year precedes publication")

    landmark_year = publication_year + landmark_age
    target_end_year = landmark_year + horizon_years
    eligible = observation_end_year >= target_end_year

    early = [
        int(counts_by_year.get(year, 0))
        for year in range(publication_year, landmark_year + 1)
    ]
    if any(v < 0 for v in early):
        raise ValueError("negative citation count")

    features = citation_features(early)

    full_metrics = paper_metrics(
        paper_id,
        publication_year,
        counts_by_year,
        observation_end_year=observation_end_year,
    )
    awakening_age = int(full_metrics["awakening_age"])
    peak_age = int(full_metrics["peak_citation_age"])
    beauty = float(full_metrics["beauty_coefficient"])

    outcome_awakening_after_landmark = int(
        eligible and landmark_age < awakening_age <= landmark_age + horizon_years
    )
    outcome_peak_after_landmark = int(
        eligible and landmark_age < peak_age <= landmark_age + horizon_years
    )

    return {
        "paper_id": paper_id,
        "openalex_id": openalex_id,
        "publication_year": publication_year,
        "landmark_age": landmark_age,
        "landmark_year": landmark_year,
        "horizon_years": horizon_years,
        "target_end_year": target_end_year,
        "observation_end_year": observation_end_year,
        "eligible_for_horizon": int(eligible),
        **features,
        "outcome_full_history_beauty_coefficient": beauty,
        "outcome_full_history_awakening_age": awakening_age,
        "outcome_full_history_peak_age": peak_age,
        "outcome_awakening_within_horizon_after_landmark": (
            outcome_awakening_after_landmark if eligible else ""
        ),
        "outcome_peak_within_horizon_after_landmark": (
            outcome_peak_after_landmark if eligible else ""
        ),
        "censor_time_from_landmark_years": max(
            0, observation_end_year - landmark_year
        ),
    }


def load_histories(rows: list[dict[str, str]]):
    histories: dict[str, dict[str, Any]] = {}
    seen: set[tuple[str, int]] = set()
    for row in rows:
        pid = (row.get("paper_id") or "").strip()
        if not pid:
            raise ValueError("paper_id required")
        pub = int(row["publication_year"])
        year = int(row["citation_year"])
        count = int(row["citations"])
        if year < pub:
            raise ValueError(f"{pid}: citation year before publication")
        if count < 0:
            raise ValueError(f"{pid}: negative citations")
        key = (pid, year)
        if key in seen:
            raise ValueError(f"duplicate paper/year row: {key}")
        seen.add(key)
        rec = histories.setdefault(
            pid,
            {
                "publication_year": pub,
                "openalex_id": row.get("openalex_id") or "",
                "counts": {},
            },
        )
        if rec["publication_year"] != pub:
            raise ValueError(f"{pid}: inconsistent publication_year")
        rec["counts"][year] = count
    return histories


def build_dataset(
    rows: list[dict[str, str]],
    *,
    landmark_age: int,
    horizon_years: int,
    observation_end_year: int | None = None,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    histories = load_histories(rows)
    output = []

    for pid in sorted(histories):
        rec = histories[pid]
        inferred_end = (
            max(rec["counts"]) if rec["counts"] else rec["publication_year"]
        )
        end = observation_end_year if observation_end_year is not None else inferred_end
        row = build_landmark_row(
            pid,
            rec["publication_year"],
            rec["counts"],
            landmark_age=landmark_age,
            horizon_years=horizon_years,
            observation_end_year=end,
            openalex_id=rec["openalex_id"],
        )
        output.append(row)

    eligible = [r for r in output if int(r["eligible_for_horizon"]) == 1]
    summary = {
        "classification": "SB1_LANDMARK_DATASET_NOT_CAUSAL_SUPPRESSION",
        "papers_total": len(output),
        "papers_eligible_for_horizon": len(eligible),
        "landmark_age": landmark_age,
        "horizon_years": horizon_years,
        "observation_end_year_override": observation_end_year,
        "eligible_outcomes": {
            "awakening_after_landmark_within_horizon": sum(
                int(r["outcome_awakening_within_horizon_after_landmark"])
                for r in eligible
            ),
            "late_peak_after_landmark_within_horizon": sum(
                int(r["outcome_peak_within_horizon_after_landmark"])
                for r in eligible
            ),
        },
        "feature_boundary": (
            "All feature_* columns use annual citations only through landmark age."
        ),
        "outcome_boundary": (
            "Full-history Beauty Coefficient, awakening age and peak age are outcomes only."
        ),
        "warnings": [
            "The binary awakening/late-peak outcomes are engineering targets, not universal Sleeping Beauty labels.",
            "No natural Beauty Coefficient cutoff is imposed.",
            "Papers without follow-up through landmark+horizon are censored and have blank binary outcomes.",
            "Semantic/network predictors must later be frozen at the same landmark date to avoid future leakage.",
        ],
    }
    return output, summary


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("citation_history_csv", type=Path)
    p.add_argument("output_csv", type=Path)
    p.add_argument("summary_json", type=Path)
    p.add_argument("--landmark-age", type=int, default=5)
    p.add_argument("--horizon-years", type=int, default=10)
    p.add_argument("--observation-end-year", type=int)
    args = p.parse_args()

    with args.citation_history_csv.open(
        "r", encoding="utf-8-sig", newline=""
    ) as f:
        rows = list(csv.DictReader(f))

    dataset, summary = build_dataset(
        rows,
        landmark_age=args.landmark_age,
        horizon_years=args.horizon_years,
        observation_end_year=args.observation_end_year,
    )
    write_csv(args.output_csv, dataset)
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
