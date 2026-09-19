#!/usr/bin/env python3
"""Zero-error anchor-panel design for AI calibration.

For n independent calibration anchors with zero observed classification errors,
the exact one-sided upper confidence bound on the true error rate is:

    upper = 1 - alpha ** (1 / n)

where alpha = 1 - confidence.

This is a design calculation only. It does not estimate actual model accuracy
and does not account for anchor clustering/dependence, which generally reduces
effective information.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


def zero_error_upper_bound(
    n: int,
    *,
    confidence: float = 0.95,
) -> float:
    if n <= 0:
        raise ValueError("n must be positive")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    alpha = 1.0 - confidence
    return 1.0 - alpha ** (1.0 / n)


def required_n_for_zero_error_bound(
    target_error_rate: float,
    *,
    confidence: float = 0.95,
) -> int:
    if not 0 < target_error_rate < 1:
        raise ValueError("target_error_rate must be between 0 and 1")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    alpha = 1.0 - confidence
    # Need 1 - alpha^(1/n) <= target
    # alpha^(1/n) >= 1-target
    # n >= log(alpha)/log(1-target)
    return math.ceil(math.log(alpha) / math.log(1.0 - target_error_rate))


def specificity_from_fpr(fpr: float) -> float:
    return 1.0 - fpr


def ppv(prevalence: float, sensitivity: float, specificity: float) -> float:
    if not 0 < prevalence < 1:
        raise ValueError("prevalence must be between 0 and 1")
    if not 0 <= sensitivity <= 1 or not 0 <= specificity <= 1:
        raise ValueError("sensitivity/specificity must be in [0,1]")
    numerator = sensitivity * prevalence
    denominator = numerator + (1.0 - specificity) * (1.0 - prevalence)
    return numerator / denominator if denominator > 0 else 0.0


def build_design(
    *,
    confidence: float = 0.95,
    error_targets: list[float] | None = None,
    prevalence_scenarios: list[float] | None = None,
    sensitivity_scenarios: list[float] | None = None,
) -> dict:
    error_targets = error_targets or [0.01, 0.005, 0.001, 0.0005, 0.0001]
    prevalence_scenarios = prevalence_scenarios or [0.002, 0.005, 0.01]
    sensitivity_scenarios = sensitivity_scenarios or [0.8, 0.9, 0.95]

    zero_error = []
    for error in error_targets:
        n = required_n_for_zero_error_bound(error, confidence=confidence)
        zero_error.append({
            "target_error_rate": error,
            "target_specificity_if_fpr": specificity_from_fpr(error),
            "required_independent_zero_error_anchors": n,
            "achieved_upper_bound_at_n": zero_error_upper_bound(
                n, confidence=confidence
            ),
        })

    ppv_rows = []
    for prevalence in prevalence_scenarios:
        for sensitivity in sensitivity_scenarios:
            for fpr in [0.01, 0.005, 0.001, 0.0005]:
                spec = 1.0 - fpr
                ppv_rows.append({
                    "true_prevalence": prevalence,
                    "sensitivity": sensitivity,
                    "specificity": spec,
                    "ppv": ppv(prevalence, sensitivity, spec),
                })

    return {
        "classification": "CALIBRATION_ANCHOR_ZERO_ERROR_DESIGN_NOT_MODEL_ACCURACY",
        "confidence": confidence,
        "zero_error_design": zero_error,
        "ppv_scenarios": ppv_rows,
        "warnings": [
            "These calculations assume independent anchor errors.",
            "Anchor clustering or near-duplicate evidence reduces effective sample size.",
            "Zero observed errors do not imply zero true error rate.",
            "A modest negative-anchor panel cannot empirically establish 99.9-99.99% specificity.",
            "Final prevalence inference must combine empirical calibration with specificity/shared-error sensitivity.",
        ],
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("output_json", type=Path)
    p.add_argument("--confidence", type=float, default=0.95)
    args = p.parse_args()

    result = build_design(confidence=args.confidence)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
