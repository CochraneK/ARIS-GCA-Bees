"""Offline reanalysis of an existing Pilot-M artifact.

This avoids re-querying OpenAlex when the acquired cohort is already sufficient
for design comparisons. It reconstructs MechanismPaper rows from the saved
cohort records and recomputes the event-time risk-set contrast under a frozen
primary case set.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from mechanism_matching import MechanismPaper
from risk_set_matching import (
    build_awakening_risk_set_contrast,
    is_at_risk_dormant_control,
    risk_set_distance,
)


def _mechanism_rows(payload: dict) -> list[MechanismPaper]:
    rows: list[MechanismPaper] = []
    for record in payload.get("records", []):
        state = record.get("state")
        if state not in {
            "SLEEPING_BEAUTY",
            "FORGOTTEN",
            "IMMEDIATE_HIT",
            "FADING",
            "AMBIGUOUS",
            "LOW_EARLY_HIGH_LATE_UNCONFIRMED",
        }:
            continue
        mechanism_state = record.get("mechanism_state") or {}
        robust = record.get("robust_sb_gate") or {}
        van_raan = robust.get("van_raan") or {}
        rows.append(
            MechanismPaper(
                paper_id=str(record["paper_id"]),
                state=str(state),
                publication_year=int(record["publication_year"]),
                field=str(record["field"]),
                early_citation_percentile=float(
                    mechanism_state.get("early_percentile", 0.0)
                ),
                reference_count=record.get("reference_count"),
                author_count=record.get("author_count"),
                early_citation_count=record.get("early_citation_count"),
                source_id=record.get("source_id"),
                annual_citation_counts=tuple(
                    int(x) for x in record["annual_citation_counts"]
                ),
                robust_sleep_years=(
                    int(van_raan["sleep_years"])
                    if robust.get("robust_sb")
                    and van_raan.get("sleep_years") is not None
                    else None
                ),
                robust_sleep_rate=(
                    float(van_raan["sleep_rate"])
                    if robust.get("robust_sb")
                    and van_raan.get("sleep_rate") is not None
                    else None
                ),
            )
        )
    return rows


def _known_case_ids(payload: dict) -> set[str]:
    ids = {
        str(row["openalex_id"])
        for row in payload.get("known_case_assessment", [])
        if row.get("openalex_id")
    }
    if not ids:
        ids.update(
            str(x)
            for x in (payload.get("pilot_design") or {}).get(
                "primary_risk_set_case_ids", []
            )
        )
    if not ids:
        raise ValueError("No frozen literature-known case IDs found")
    return ids


def _quantile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return float(ordered[0])
    pos = p * (len(ordered) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(ordered) - 1)
    frac = pos - lo
    return float(ordered[lo] * (1.0 - frac) + ordered[hi] * frac)


def _support_diagnostics(
    papers: list[MechanismPaper],
    case_ids: set[str],
) -> dict:
    by_id = {p.paper_id: p for p in papers}
    out = {}
    for case_id in sorted(case_ids):
        case = by_id[case_id]
        eligible = []
        for control in papers:
            ok, rate, burst = is_at_risk_dormant_control(case, control)
            if not ok or rate is None:
                continue
            eligible.append(
                {
                    "control_id": control.paper_id,
                    "sleep_rate": float(rate),
                    "sleep_gap": abs(float(case.robust_sleep_rate) - float(rate)),
                    "reference_gap": (
                        abs(float(case.reference_count) - float(control.reference_count))
                        if case.reference_count is not None
                        and control.reference_count is not None
                        else None
                    ),
                    "author_gap": (
                        abs(float(case.author_count) - float(control.author_count))
                        if case.author_count is not None
                        and control.author_count is not None
                        else None
                    ),
                    "distance": risk_set_distance(
                        case,
                        control,
                        control_rate=float(rate),
                    ),
                    "future_state": control.state,
                    "first_burst_age": burst,
                }
            )
        eligible.sort(key=lambda x: (x["distance"], x["control_id"]))
        sleep_gaps = [x["sleep_gap"] for x in eligible]
        ref_gaps = [
            x["reference_gap"] for x in eligible
            if x["reference_gap"] is not None
        ]
        author_gaps = [
            x["author_gap"] for x in eligible
            if x["author_gap"] is not None
        ]
        out[case_id] = {
            "case_event_age": case.robust_sleep_years,
            "case_sleep_rate": case.robust_sleep_rate,
            "case_reference_count": case.reference_count,
            "case_author_count": case.author_count,
            "n_eligible_controls_in_acquired_cohort": len(eligible),
            "sleep_gap": {
                "min": min(sleep_gaps) if sleep_gaps else None,
                "p10": _quantile(sleep_gaps, 0.10),
                "p25": _quantile(sleep_gaps, 0.25),
                "median": _quantile(sleep_gaps, 0.50),
            },
            "reference_gap_min": min(ref_gaps) if ref_gaps else None,
            "author_gap_min": min(author_gaps) if author_gaps else None,
            "nearest_controls": eligible[:10],
        }
    return out


def reanalyze(payload: dict, ratios: list[int]) -> dict:
    papers = _mechanism_rows(payload)
    case_ids = _known_case_ids(payload)
    contrasts = {}
    for ratio in ratios:
        contrast = build_awakening_risk_set_contrast(
            papers,
            controls_per_case=ratio,
            case_ids=case_ids,
            with_replacement_across_risk_sets=True,
            max_sleep_rate=2.0,
            wake_years=4,
            min_wake_rate=5.0,
            max_abs_smd=0.10,
        )
        contrasts[f"1:{ratio}"] = contrast
    return {
        "analysis": "offline frozen-known-case risk-set reanalysis",
        "source_pilot_design": payload.get("pilot_design"),
        "n_source_records": len(payload.get("records", [])),
        "n_reconstructed_rows": len(papers),
        "frozen_primary_case_ids": sorted(case_ids),
        "control_reuse_across_case_risk_sets": True,
        "balance_threshold_abs_smd": 0.10,
        "support_diagnostics": _support_diagnostics(papers, case_ids),
        "contrasts": contrasts,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ratios", default="1,4")
    args = parser.parse_args()
    ratios = [int(x) for x in args.ratios.split(",") if x.strip()]
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    result = reanalyze(payload, ratios)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
