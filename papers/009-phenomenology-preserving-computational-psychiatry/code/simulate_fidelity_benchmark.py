#!/usr/bin/env python3
"""Synthetic engineering simulation for ARIS4C009A.

The numbers below are deliberately hypothetical. They test code paths and study
logic only; they are not empirical estimates and must never be cited as findings.
"""

from __future__ import annotations

import argparse
import math
import random
from collections import defaultdict
from dataclasses import dataclass


DOMAINS = ("concrete", "agency", "minimal_self", "context", "temporal")


@dataclass(frozen=True)
class Spec:
    probabilities: tuple[float, ...]
    burden_minutes: float


SPECS = {
    "R0_rich_source": Spec((0.96, 0.94, 0.92, 0.96, 0.94), 120.0),
    "R1_episode_graph": Spec((0.92, 0.90, 0.88, 0.91, 0.90), 45.0),
    "R2_expert_phenomenology": Spec((0.89, 0.91, 0.90, 0.86, 0.87), 60.0),
    "R3_self_report": Spec((0.82, 0.67, 0.61, 0.63, 0.69), 8.0),
    "R4_symptom_scale": Spec((0.86, 0.62, 0.50, 0.48, 0.58), 15.0),
    "R5_low_dimensional": Spec((0.74, 0.58, 0.48, 0.45, 0.52), 3.0),
}


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)


def standard_error(p: float, n: int) -> float:
    return math.sqrt(p * (1.0 - p) / n)


def simulate(
    episodes: int = 300,
    queries_per_domain: int = 8,
    seed: int = 20260918,
) -> dict[str, dict[str, float]]:
    rng = random.Random(seed)
    result: dict[str, dict[str, float]] = {}

    for name, spec in SPECS.items():
        domain_accuracy: dict[str, float] = {}
        n = episodes * queries_per_domain

        for idx, domain in enumerate(DOMAINS):
            successes = sum(
                rng.random() < spec.probabilities[idx]
                for _ in range(n)
            )
            domain_accuracy[domain] = successes / n

        overall = mean(list(domain_accuracy.values()))
        result[name] = {
            **domain_accuracy,
            "overall": overall,
            "burden_minutes": spec.burden_minutes,
            "approx_se": standard_error(overall, n * len(DOMAINS)),
        }

    return result


def dominates(a: dict[str, float], b: dict[str, float]) -> bool:
    """Two-axis engineering dominance: overall fidelity high, burden low."""
    weakly_better = (
        a["overall"] >= b["overall"]
        and a["burden_minutes"] <= b["burden_minutes"]
    )
    strictly_better = (
        a["overall"] > b["overall"]
        or a["burden_minutes"] < b["burden_minutes"]
    )
    return weakly_better and strictly_better


def frontier(result: dict[str, dict[str, float]]) -> list[str]:
    return [
        name
        for name, values in result.items()
        if not any(
            dominates(other_values, values)
            for other_name, other_values in result.items()
            if other_name != name
        )
    ]


def format_table(result: dict[str, dict[str, float]]) -> str:
    columns = ("representation", *DOMAINS, "overall", "burden_min")
    rows = ["\t".join(columns)]
    for name, values in result.items():
        rows.append(
            "\t".join(
                [
                    name,
                    *(f"{values[d]:.3f}" for d in DOMAINS),
                    f"{values['overall']:.3f}",
                    f"{values['burden_minutes']:.1f}",
                ]
            )
        )
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episodes", type=int, default=300)
    parser.add_argument("--queries-per-domain", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260918)
    args = parser.parse_args()

    result = simulate(
        episodes=args.episodes,
        queries_per_domain=args.queries_per_domain,
        seed=args.seed,
    )

    print("SYNTHETIC ENGINEERING OUTPUT — NOT EMPIRICAL EVIDENCE")
    print(format_table(result))
    print("\nTwo-axis synthetic Pareto frontier:")
    for name in frontier(result):
        print(f"- {name}")


if __name__ == "__main__":
    main()
