#!/usr/bin/env python3
"""Design analysis for AI adjudicator measurement error in ARIS4C005.

This is not an empirical estimate of model accuracy. It quantifies how assumed
sensitivity/specificity interact with rare article-level prevalence, and why
AI consensus must be calibrated rather than treated as truth."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def metrics(prevalence: float, sensitivity: float, specificity: float):
    p = prevalence
    se = sensitivity
    sp = specificity
    fpr = 1.0 - sp
    observed_positive = se * p + fpr * (1.0 - p)
    ppv = (se * p / observed_positive) if observed_positive > 0 else None
    observed_negative = (1.0 - se) * p + sp * (1.0 - p)
    npv = (sp * (1.0 - p) / observed_negative) if observed_negative > 0 else None
    return {
        "true_prevalence": p,
        "sensitivity": se,
        "specificity": sp,
        "observed_positive_rate": observed_positive,
        "ppv": ppv,
        "npv": npv,
        "false_positive_share_among_positive": (1.0 - ppv) if ppv is not None else None,
    }


def min_specificity_for_ppv(prevalence: float, sensitivity: float, target_ppv: float) -> float:
    p = prevalence
    se = sensitivity
    t = target_ppv
    if not (0 < p < 1 and 0 < se <= 1 and 0 < t < 1):
        raise ValueError("invalid inputs")
    max_fpr = se * p * (1.0 - t) / (t * (1.0 - p))
    return max(0.0, min(1.0, 1.0 - max_fpr))


def independent_and_consensus(prevalence: float, sensitivity: float, specificity: float):
    """Optimistic conditional-independence sensitivity for two identical adjudicators."""
    se2 = sensitivity * sensitivity
    fpr = 1.0 - specificity
    sp2 = 1.0 - fpr * fpr
    out = metrics(prevalence, se2, sp2)
    out["assumption"] = "CONDITIONAL_INDEPENDENCE_OPTIMISTIC"
    out["single_model_sensitivity"] = sensitivity
    out["single_model_specificity"] = specificity
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("output_json", type=Path)
    p.add_argument("--prevalence", action="append", type=float, default=[])
    p.add_argument("--sensitivity", action="append", type=float, default=[])
    p.add_argument("--specificity", action="append", type=float, default=[])
    args = p.parse_args()

    prevalences = args.prevalence or [0.002, 0.005, 0.01, 0.02]
    sensitivities = args.sensitivity or [0.80, 0.90, 0.95]
    specificities = args.specificity or [0.95, 0.98, 0.99, 0.995, 0.999]

    scenarios = []
    consensus = []
    for prevalence in prevalences:
        for sensitivity in sensitivities:
            for specificity in specificities:
                scenarios.append(metrics(prevalence, sensitivity, specificity))
                consensus.append(independent_and_consensus(prevalence, sensitivity, specificity))

    requirements = []
    for prevalence in prevalences:
        for sensitivity in sensitivities:
            for target_ppv in (0.50, 0.80, 0.90):
                requirements.append({
                    "true_prevalence": prevalence,
                    "assumed_sensitivity": sensitivity,
                    "target_ppv": target_ppv,
                    "minimum_specificity": min_specificity_for_ppv(prevalence, sensitivity, target_ppv),
                })

    output = {
        "classification": "AI_ADJUDICATOR_ERROR_DESIGN_SCENARIOS_NOT_EMPIRICAL_ACCURACY",
        "single_model_scenarios": scenarios,
        "two_model_and_consensus_optimistic": consensus,
        "specificity_requirements": requirements,
        "warnings": [
            "Sensitivity and specificity are hypothetical design inputs, not measured model performance.",
            "Two-model consensus calculations assume conditional independence and are optimistic when model errors correlate.",
            "Rare prevalence makes specificity especially important because false positives can dominate observed positives.",
            "Calibration anchors and disagreement/abstention rates must be estimated in the actual adjudication workflow.",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
