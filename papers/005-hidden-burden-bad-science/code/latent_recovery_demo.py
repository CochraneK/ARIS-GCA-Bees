#!/usr/bin/env python3
"""Six-stratum synthetic recovery demo for ARIS4C005 latent prevalence.

This validates implementation under known simulated truth. It is not empirical
evidence about bad-science prevalence and does not validate the real-world
conditional-independence assumption.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

from latent_prevalence import fit


def bernoulli(rng: random.Random, p: float) -> int:
    return 1 if rng.random() < p else 0


def simulate_measurement(
    rng: random.Random,
    z: int,
    se: float,
    sp: float,
    missing_rate: float,
) -> str:
    if rng.random() < missing_rate:
        return ""
    if z == 1:
        return "1" if rng.random() < se else "0"
    return "0" if rng.random() < sp else "1"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("scaled_summary_json", type=Path)
    p.add_argument("output_json", type=Path)
    p.add_argument("--seed", type=int, default=20260918)
    args = p.parse_args()

    scaled = json.loads(args.scaled_summary_json.read_text(encoding="utf-8"))
    strata = scaled["strata"]
    names = list(strata)

    # Deliberately modest heterogeneity around a rare global rate.
    true_p = {
        name: 0.003 + i * 0.001
        for i, name in enumerate(names)
    }

    se_a, sp_a = 0.90, 0.9990
    se_b, sp_b = 0.92, 0.9995
    missing_a, missing_b = 0.03, 0.04
    rng = random.Random(args.seed)

    rows = []
    paper = 0
    for name in names:
        n = int(strata[name]["target_n"])
        N = int(strata[name]["population_N"])
        for _ in range(n):
            paper += 1
            z = bernoulli(rng, true_p[name])
            rows.append(
                {
                    "paper_id": f"SYN{paper}",
                    "audit_stratum": name,
                    "stratum_population_N": str(N),
                    "a_binary_severe": simulate_measurement(
                        rng, z, se_a, sp_a, missing_a
                    ),
                    "b_binary_severe": simulate_measurement(
                        rng, z, se_b, sp_b, missing_b
                    ),
                }
            )

    calibration = {
        "AI_A": {
            "tp": 9000,
            "fn": 1000,
            "tn": 999000,
            "fp": 1000,
        },
        "AI_B": {
            "tp": 9200,
            "fn": 800,
            "tn": 999500,
            "fp": 500,
        },
    }

    result = fit(
        rows,
        calibration,
        draws=1200,
        seed=args.seed + 99,
        grid_points=900,
        p_max=0.03,
    )

    total_N = sum(int(strata[name]["population_N"]) for name in names)
    true_global = sum(
        int(strata[name]["population_N"]) / total_N * true_p[name]
        for name in names
    )

    recovered = result["global_prevalence"]
    output = {
        "classification": "SYNTHETIC_LATENT_MODEL_RECOVERY_NOT_EMPIRICAL_PREVALENCE",
        "simulation": {
            "seed": args.seed,
            "true_stratum_prevalence": true_p,
            "true_global_prevalence": true_global,
            "se_a": se_a,
            "sp_a": sp_a,
            "se_b": se_b,
            "sp_b": sp_b,
            "missing_a": missing_a,
            "missing_b": missing_b,
            "sample_rows": len(rows),
        },
        "recovered_global_prevalence": recovered,
        "absolute_median_error": abs(recovered["median"] - true_global),
        "true_value_inside_95_interval": (
            recovered["q025"] <= true_global <= recovered["q975"]
        ),
        "model_measurement_posterior": result["measurement_posterior"],
        "warnings": [
            "Synthetic recovery checks code implementation under the model assumptions.",
            "It does not prove AI errors are conditionally independent in real data.",
            "It does not estimate real research-integrity prevalence.",
        ],
    }

    # Engineering gate, intentionally modest because one finite synthetic draw
    # can deviate from truth even when the estimator is correct.
    if output["absolute_median_error"] > 0.003:
        raise SystemExit(
            f"Synthetic recovery median error too large: {output['absolute_median_error']}"
        )
    if not output["true_value_inside_95_interval"]:
        raise SystemExit("Synthetic truth not inside recovered 95% interval")

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
