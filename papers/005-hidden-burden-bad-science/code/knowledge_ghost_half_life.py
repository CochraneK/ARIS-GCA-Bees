#!/usr/bin/env python3
"""Estimate descriptive Citation Ghost Half-Life for ARIS4C005.

Input is the source-level CSV produced by build_contamination_exposure.py.

This module estimates a citation-exposure decay measure, not semantic
contamination decay. For each source:

1) baseline = mean annual citation count in up to K complete calendar years
   before the retraction year;
2) threshold = 50% of baseline;
3) half-life event = first complete post-retraction calendar year at or below
   threshold, requiring confirm_years consecutive years at/below threshold;
4) if no event is observed before the final complete observation year, the
   source is right-censored.

The retraction calendar year is excluded from baseline and event detection
because publication/retraction can occur mid-year."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import statistics
from pathlib import Path
from typing import Any


def load_year_counts(raw: str) -> dict[int, int]:
    data = json.loads(raw or "{}")
    return {int(k): int(v) for k, v in data.items()}


def full_post_years(retraction_year: int, last_complete_year: int) -> list[int]:
    if last_complete_year <= retraction_year:
        return []
    return list(range(retraction_year + 1, last_complete_year + 1))


def source_half_life(
    counts: dict[int, int],
    retraction_date: dt.date,
    *,
    baseline_years: int = 3,
    confirm_years: int = 2,
    last_complete_year: int,
) -> dict[str, Any]:
    ry = retraction_date.year
    pre_candidates = [y for y in sorted(counts) if y < ry]
    pre = pre_candidates[-baseline_years:]

    if not pre:
        return {"estimable": False, "reason": "NO_PRE_RETRACTION_BASELINE"}

    baseline_values = [counts.get(y, 0) for y in pre]
    baseline = statistics.mean(baseline_values)
    if baseline <= 0:
        return {
            "estimable": False,
            "reason": "ZERO_PRE_RETRACTION_BASELINE",
            "baseline_years": pre,
            "baseline_mean": baseline,
        }

    threshold = baseline * 0.5
    post_years = full_post_years(ry, last_complete_year)
    if len(post_years) < confirm_years:
        return {
            "estimable": False,
            "reason": "INSUFFICIENT_COMPLETE_POST_RETRACTION_YEARS",
            "baseline_years": pre,
            "baseline_mean": baseline,
            "threshold": threshold,
        }

    event_year = None
    for i in range(0, len(post_years) - confirm_years + 1):
        window = post_years[i:i + confirm_years]
        if all(counts.get(y, 0) <= threshold for y in window):
            event_year = window[0]
            break

    if event_year is not None:
        return {
            "estimable": True,
            "event_observed": True,
            "baseline_years": pre,
            "baseline_mean": baseline,
            "threshold": threshold,
            "half_life_years": event_year - ry,
            "event_year": event_year,
            "last_complete_year": last_complete_year,
        }

    return {
        "estimable": True,
        "event_observed": False,
        "right_censored": True,
        "baseline_years": pre,
        "baseline_mean": baseline,
        "threshold": threshold,
        "censor_time_years": last_complete_year - ry,
        "last_complete_year": last_complete_year,
    }


def kaplan_meier_median(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Simple Kaplan-Meier median for integer-year event/censor times."""
    observations = []
    for r in records:
        if not r.get("estimable"):
            continue
        if r.get("event_observed"):
            observations.append((int(r["half_life_years"]), True))
        elif r.get("right_censored"):
            observations.append((int(r["censor_time_years"]), False))

    if not observations:
        return {
            "n": 0,
            "median_years": None,
            "median_reached": False,
            "survival_curve": [],
        }

    times = sorted({t for t, _ in observations})
    survival = 1.0
    curve = []
    median = None

    for t in times:
        at_risk = sum(1 for time, _ in observations if time >= t)
        events = sum(1 for time, event in observations if time == t and event)
        censored = sum(1 for time, event in observations if time == t and not event)
        if at_risk > 0 and events > 0:
            survival *= 1.0 - events / at_risk
        curve.append({
            "time_years": t,
            "at_risk": at_risk,
            "events": events,
            "censored": censored,
            "survival": survival,
        })
        if median is None and survival <= 0.5:
            median = t

    return {
        "n": len(observations),
        "events": sum(1 for _, event in observations if event),
        "censored": sum(1 for _, event in observations if not event),
        "median_years": median,
        "median_reached": median is not None,
        "survival_curve": curve,
    }


def summarize_sources(rows, *, baseline_years: int, confirm_years: int, last_complete_year: int):
    records = []
    reasons = {}
    for row in rows:
        ret = dt.date.fromisoformat(row["source_retraction_date"])
        counts = load_year_counts(row["citation_counts_by_year_json"])
        result = source_half_life(
            counts, ret,
            baseline_years=baseline_years,
            confirm_years=confirm_years,
            last_complete_year=last_complete_year,
        )
        result["source_openalex_id"] = row.get("source_openalex_id", "")
        records.append(result)
        if not result.get("estimable"):
            reason = str(result.get("reason") or "UNKNOWN")
            reasons[reason] = reasons.get(reason, 0) + 1

    km = kaplan_meier_median(records)
    return {
        "classification": "CITATION_GHOST_HALF_LIFE_DESCRIPTIVE_NOT_SEMANTIC_CONTAMINATION",
        "definition": {
            "baseline_years": baseline_years,
            "threshold_fraction": 0.5,
            "confirm_years": confirm_years,
            "retraction_year_excluded": True,
            "last_complete_year": last_complete_year,
        },
        "sources_total": len(rows),
        "sources_estimable": sum(bool(r.get("estimable")) for r in records),
        "sources_not_estimable_by_reason": reasons,
        "kaplan_meier": km,
        "warnings": [
            "This is citation-exposure decay, not material-dependence decay.",
            "The high-propagation source pilot is not representative of all problematic papers.",
            "Calendar-year aggregation creates interval coarsening around exact retraction dates.",
            "OpenAlex citation matching can miss printed references.",
            "A semantic Dependence Ghost Half-Life requires adjudicated citation contexts.",
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("sources_csv", type=Path)
    p.add_argument("output_json", type=Path)
    p.add_argument("--baseline-years", type=int, default=3)
    p.add_argument("--confirm-years", type=int, default=2)
    p.add_argument("--last-complete-year", type=int, default=dt.date.today().year - 1)
    args = p.parse_args()

    with args.sources_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    result = summarize_sources(
        rows,
        baseline_years=args.baseline_years,
        confirm_years=args.confirm_years,
        last_complete_year=args.last_complete_year,
    )
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
