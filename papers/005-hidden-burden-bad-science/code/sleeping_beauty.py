#!/usr/bin/env python3
"""Historical delayed-recognition metrics for ARIS4C005.

Implements the parameter-free Beauty Coefficient B and awakening age t_a from
Ke et al. (PNAS 2015). Outputs continuous measures by default.

Any percentile Sleeping Beauty flag is sample-relative and exploratory; there is
no natural universal threshold in the original result.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any


def annual_series(
    publication_year: int,
    citation_counts_by_year: dict[int, int],
    observation_end_year: int | None = None,
) -> list[int]:
    if observation_end_year is None:
        observation_end_year = max(
            [publication_year, *citation_counts_by_year.keys()]
        )
    if observation_end_year < publication_year:
        raise ValueError("observation_end_year precedes publication")
    out = []
    for year in range(publication_year, observation_end_year + 1):
        value = int(citation_counts_by_year.get(year, 0))
        if value < 0:
            raise ValueError("citation counts cannot be negative")
        out.append(value)
    return out


def peak_age(citations: list[int]) -> int:
    if not citations:
        raise ValueError("citation series is empty")
    peak = max(citations)
    # Frozen tie rule: earliest maximum. This avoids artificially extending
    # sleep when the same annual maximum occurs in several later years.
    return citations.index(peak)


def beauty_coefficient(citations: list[int]) -> float:
    if not citations:
        raise ValueError("citation series is empty")
    tm = peak_age(citations)
    if tm == 0:
        return 0.0

    c0 = float(citations[0])
    cm = float(citations[tm])
    slope = (cm - c0) / tm

    b = 0.0
    for t in range(tm + 1):
        ct = float(citations[t])
        line = slope * t + c0
        b += (line - ct) / max(1.0, ct)
    return b


def awakening_age(citations: list[int]) -> int:
    if not citations:
        raise ValueError("citation series is empty")
    tm = peak_age(citations)
    if tm == 0:
        return 0

    c0 = float(citations[0])
    cm = float(citations[tm])
    denominator = math.sqrt((cm - c0) ** 2 + tm ** 2)
    if denominator == 0:
        return 0

    distances = []
    for t in range(tm + 1):
        ct = float(citations[t])
        numerator = abs((cm - c0) * t - tm * ct + tm * c0)
        distances.append(numerator / denominator)

    # Frozen tie rule: earliest maximal distance.
    return distances.index(max(distances))


def paper_metrics(
    paper_id: str,
    publication_year: int,
    citation_counts_by_year: dict[int, int],
    observation_end_year: int | None = None,
) -> dict[str, Any]:
    citations = annual_series(
        publication_year,
        citation_counts_by_year,
        observation_end_year,
    )
    tm = peak_age(citations)
    ta = awakening_age(citations)
    b = beauty_coefficient(citations)

    return {
        "paper_id": paper_id,
        "publication_year": publication_year,
        "observation_end_year": publication_year + len(citations) - 1,
        "observation_years_including_publication": len(citations),
        "total_citations_observed": sum(citations),
        "peak_citation_age": tm,
        "peak_citations_per_year": citations[tm],
        "awakening_age": ta,
        "awakening_year": publication_year + ta,
        "beauty_coefficient": b,
    }


def percentile(values: list[float], value: float) -> float:
    """Empirical <= percentile, deterministic with ties."""
    if not values:
        raise ValueError("values empty")
    return sum(v <= value for v in values) / len(values)


def analyze(
    rows: list[dict[str, str]],
    *,
    top_fraction: float | None = None,
) -> dict[str, Any]:
    histories: dict[str, dict[str, Any]] = {}
    seen_years: set[tuple[str, int]] = set()

    for row in rows:
        pid = (row.get("paper_id") or "").strip()
        if not pid:
            raise ValueError("paper_id required")
        publication_year = int(row["publication_year"])
        citation_year = int(row["citation_year"])
        citations = int(row["citations"])
        if citation_year < publication_year:
            raise ValueError(f"{pid}: citation year before publication")
        if citations < 0:
            raise ValueError(f"{pid}: negative citations")

        key = (pid, citation_year)
        if key in seen_years:
            raise ValueError(f"duplicate paper/year citation row: {key}")
        seen_years.add(key)

        rec = histories.setdefault(
            pid,
            {
                "publication_year": publication_year,
                "openalex_id": row.get("openalex_id") or "",
                "counts": {},
            },
        )
        if rec["publication_year"] != publication_year:
            raise ValueError(f"{pid}: inconsistent publication_year")
        rec["counts"][citation_year] = citations

    metrics = []
    for pid, rec in histories.items():
        end = max(rec["counts"]) if rec["counts"] else rec["publication_year"]
        m = paper_metrics(
            pid,
            rec["publication_year"],
            rec["counts"],
            observation_end_year=end,
        )
        m["openalex_id"] = rec["openalex_id"]
        metrics.append(m)

    b_values = [float(m["beauty_coefficient"]) for m in metrics]
    for m in metrics:
        m["beauty_percentile_within_input"] = percentile(
            b_values,
            float(m["beauty_coefficient"]),
        )

    threshold = None
    if top_fraction is not None:
        if not (0 < top_fraction < 1):
            raise ValueError("top_fraction must be between 0 and 1")
        ordered = sorted(b_values)
        index = max(0, math.ceil((1 - top_fraction) * len(ordered)) - 1)
        threshold = ordered[index]
        for m in metrics:
            m["sample_relative_sb_flag"] = int(
                float(m["beauty_coefficient"]) >= threshold
            )

    metrics.sort(
        key=lambda m: (
            float(m["beauty_coefficient"]),
            m["paper_id"],
        ),
        reverse=True,
    )

    return {
        "classification": "HISTORICAL_DELAYED_RECOGNITION_METRICS_NOT_LOST_DISCOVERY_COUNT",
        "papers": len(metrics),
        "beauty_coefficient": {
            "min": min(b_values) if b_values else None,
            "max": max(b_values) if b_values else None,
            "mean": (sum(b_values) / len(b_values)) if b_values else None,
            "continuous_primary_measure": True,
        },
        "sample_relative_flag": {
            "enabled": top_fraction is not None,
            "top_fraction": top_fraction,
            "threshold_within_input": threshold,
            "warning": (
                "This threshold is relative to the supplied dataset and is not "
                "a natural/universal Sleeping Beauty cutoff."
            ),
        },
        "paper_metrics": metrics,
        "warnings": [
            "Beauty Coefficient uses citation history only through the annual-citation peak.",
            "Recent non-awakened papers are right-censored candidates, not never-awakened discoveries.",
            "Database citation coverage affects B and awakening time.",
            "Historical delayed recognition is not evidence that integrity failures caused the delay.",
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("citation_history_csv", type=Path)
    p.add_argument("output_json", type=Path)
    p.add_argument("--top-fraction", type=float)
    args = p.parse_args()

    with args.citation_history_csv.open(
        "r", encoding="utf-8-sig", newline=""
    ) as f:
        rows = list(csv.DictReader(f))

    result = analyze(rows, top_fraction=args.top_fraction)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
