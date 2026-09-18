#!/usr/bin/env python3
"""Design-weighted calibration summary for ARIS4C005 Pilot B.

This is a calibration/diagnostic layer, not the final Bayesian latent model.
It estimates:
- design-weighted adjudicated severe prevalence;
- detector sensitivity/specificity/PPV/NPV against adjudicated resolved cases;
- detector missingness;
- effective sample size.

Rows labelled SERIOUS_UNRESOLVED or INDETERMINATE are excluded from the binary
reference-standard calculations and remain visible in the output.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

POSITIVE_REFERENCE = {"SEVERE_SUPPORTED"}
NEGATIVE_REFERENCE = {
    "HONEST_MAJOR_ERROR",
    "MINOR_OR_IMMATERIAL",
    "NO_MATERIAL_PROBLEM_FOUND",
}
UNRESOLVED_REFERENCE = {"SERIOUS_UNRESOLVED", "INDETERMINATE"}


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


def safe_div(a: float, b: float) -> float | None:
    return a / b if b > 0 else None


def kish_effective_n(weights: list[float]) -> float:
    s = sum(weights)
    s2 = sum(w * w for w in weights)
    return (s * s / s2) if s2 > 0 else 0.0


def reference_value(label: str) -> int | None:
    label = label.strip().upper()
    if label in POSITIVE_REFERENCE:
        return 1
    if label in NEGATIVE_REFERENCE:
        return 0
    if label in UNRESOLVED_REFERENCE or not label:
        return None
    raise ValueError(f"Unknown scientific_state label: {label!r}")


def summarize(
    rows: list[dict[str, str]],
    detector_cols: list[str],
    label_col: str,
    weight_col: str,
) -> dict[str, Any]:
    label_counts = Counter((r.get(label_col) or "").strip().upper() or "MISSING" for r in rows)
    resolved: list[tuple[dict[str, str], int, float]] = []

    for row in rows:
        y = reference_value(row.get(label_col) or "")
        if y is None:
            continue
        w = float(row.get(weight_col) or 0)
        if not math.isfinite(w) or w <= 0:
            raise ValueError(f"Invalid design weight {w!r}")
        resolved.append((row, y, w))

    weights = [w for _, _, w in resolved]
    total_w = sum(weights)
    severe_w = sum(w for _, y, w in resolved if y == 1)

    result: dict[str, Any] = {
        "classification": "PILOT_B_CALIBRATION_NOT_FINAL_LATENT_PREVALENCE",
        "rows_total": len(rows),
        "label_counts": dict(label_counts),
        "resolved_binary_rows": len(resolved),
        "design_weighted_severe_prevalence": safe_div(severe_w, total_w),
        "kish_effective_sample_size": kish_effective_n(weights),
        "detectors": {},
        "warnings": [
            "This output is a design-weighted calibration diagnostic, not the final latent prevalence estimate.",
            "SERIOUS_UNRESOLVED and INDETERMINATE are excluded from binary reference-standard metrics.",
            "A detector-enriched sample is valid for population inference only when inclusion probabilities/design weights are correct.",
            "Intent/guilt is not inferred from article-level detector signals.",
        ],
    }

    for detector in detector_cols:
        tp = fp = tn = fn = missing_w = observed_w = 0.0
        observed_rows = missing_rows = 0
        for row, y, w in resolved:
            d = parse_binary(row.get(detector))
            if d is None:
                missing_w += w
                missing_rows += 1
                continue
            observed_w += w
            observed_rows += 1
            if d == 1 and y == 1:
                tp += w
            elif d == 1 and y == 0:
                fp += w
            elif d == 0 and y == 0:
                tn += w
            elif d == 0 and y == 1:
                fn += w

        result["detectors"][detector] = {
            "weighted_tp": tp,
            "weighted_fp": fp,
            "weighted_tn": tn,
            "weighted_fn": fn,
            "sensitivity": safe_div(tp, tp + fn),
            "specificity": safe_div(tn, tn + fp),
            "ppv": safe_div(tp, tp + fp),
            "npv": safe_div(tn, tn + fn),
            "weighted_missing_fraction_among_resolved": safe_div(missing_w, missing_w + observed_w),
            "observed_resolved_rows": observed_rows,
            "missing_resolved_rows": missing_rows,
        }

    random_resolved = sum(
        1
        for row, y, _ in resolved
        if (row.get("aris_selected_via") or "") == "population_random"
    )
    informative_detectors = sum(
        1
        for d in result["detectors"].values()
        if d["sensitivity"] is not None and d["specificity"] is not None
    )
    result["identification_gate"] = {
        "population_random_resolved_rows": random_resolved,
        "informative_detectors": informative_detectors,
        "pilot_ready_for_latent_model": bool(random_resolved >= 100 and informative_detectors >= 1),
        "rule": "Require >=100 resolved population-random adjudications plus >=1 detector with estimable sensitivity and specificity for this dry-run gate; final gate is stricter and includes uncertainty/prior-sensitivity checks.",
    }
    return result


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("adjudicated_csv", type=Path)
    p.add_argument("output_json", type=Path)
    p.add_argument("--detector", action="append", default=[], dest="detectors")
    p.add_argument("--label-col", default="scientific_state")
    p.add_argument("--weight-col", default="aris_design_weight")
    args = p.parse_args()

    if not args.detectors:
        raise SystemExit("At least one --detector column is required.")

    with args.adjudicated_csv.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    result = summarize(rows, args.detectors, args.label_col, args.weight_col)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
