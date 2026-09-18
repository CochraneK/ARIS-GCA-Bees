#!/usr/bin/env python3
"""Synthetic power/precision sensitivity analysis for ARIS4C009A.

This is an engineering model, not an empirical estimate of psychiatric effect sizes.

The confirmatory analysis in 009A is hierarchical. This simulation deliberately uses
a simpler participant-level paired contrast as a transparent power proxy. It includes
participant, episode, query, and representation-specific evaluator heterogeneity and
is intended to show how design decisions alter precision before a pilot supplies
empirical variance components.
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Scenario:
    episodes_per_participant: int = 2
    queries_per_episode: int = 15
    baseline_accuracy: float = 0.68
    participant_sd: float = 0.60
    episode_sd: float = 0.50
    query_sd: float = 0.70
    evaluator_sd: float = 0.80


def logistic(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def logit(p: float) -> float:
    return math.log(p / (1.0 - p))


def run_cell(
    *,
    participants: int,
    target_delta: float,
    replicates: int,
    scenario: Scenario,
    rng: np.random.Generator,
) -> tuple[float, float]:
    """Return proxy rejection rate and mean observed accuracy difference.

    target_delta is specified on the marginal probability scale before random
    heterogeneity is added. Because logistic-normal mixing attenuates probability
    differences, the realized mean contrast will usually be smaller.
    """
    base_logit = logit(scenario.baseline_accuracy)
    target_p = min(max(scenario.baseline_accuracy + target_delta, 0.001), 0.999)
    representation_effect = logit(target_p) - base_logit

    rejections = 0
    observed_differences: list[float] = []

    n = participants
    e = scenario.episodes_per_participant
    q = scenario.queries_per_episode

    for _ in range(replicates):
        participant_fx = rng.normal(0.0, scenario.participant_sd, size=(n, 1, 1))
        episode_fx = rng.normal(0.0, scenario.episode_sd, size=(n, e, 1))
        query_fx = rng.normal(0.0, scenario.query_sd, size=(n, e, q))

        # Different evaluators can see different representations of the same episode.
        evaluator_r3 = rng.normal(0.0, scenario.evaluator_sd, size=(n, e, 1))
        evaluator_r2 = rng.normal(0.0, scenario.evaluator_sd, size=(n, e, 1))

        common = base_logit + participant_fx + episode_fx + query_fx
        p_r3 = logistic(common + evaluator_r3)
        p_r2 = logistic(common + representation_effect + evaluator_r2)

        y_r3 = (rng.random(size=p_r3.shape) < p_r3).astype(np.int8)
        y_r2 = (rng.random(size=p_r2.shape) < p_r2).astype(np.int8)

        participant_diffs = (y_r2 - y_r3).mean(axis=(1, 2))
        mean_diff = float(participant_diffs.mean())
        sd_diff = float(participant_diffs.std(ddof=1))

        observed_differences.append(mean_diff)

        if sd_diff > 0:
            z = mean_diff / (sd_diff / math.sqrt(n))
            if abs(z) >= 1.96:
                rejections += 1

    return rejections / replicates, float(np.mean(observed_differences))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--replicates", type=int, default=250)
    parser.add_argument("--seed", type=int, default=20260918)
    parser.add_argument(
        "--participants",
        type=int,
        nargs="+",
        default=[30, 40, 50, 60, 80, 100, 120, 160],
    )
    parser.add_argument(
        "--deltas",
        type=float,
        nargs="+",
        default=[0.03, 0.05, 0.075, 0.10],
    )
    parser.add_argument("--episodes", type=int, default=2)
    parser.add_argument("--queries", type=int, default=15)
    parser.add_argument("--baseline-accuracy", type=float, default=0.68)
    parser.add_argument("--evaluator-sd", type=float, default=0.80)
    args = parser.parse_args()

    scenario = Scenario(
        episodes_per_participant=args.episodes,
        queries_per_episode=args.queries,
        baseline_accuracy=args.baseline_accuracy,
        evaluator_sd=args.evaluator_sd,
    )

    rng = np.random.default_rng(args.seed)

    print("SYNTHETIC DESIGN SENSITIVITY — NOT EMPIRICAL POWER")
    print(
        "delta\tparticipants\tproxy_power\tmean_observed_difference"
    )

    for delta in args.deltas:
        for participants in args.participants:
            proxy_power, mean_diff = run_cell(
                participants=participants,
                target_delta=delta,
                replicates=args.replicates,
                scenario=scenario,
                rng=rng,
            )
            print(
                f"{delta:.3f}\t{participants}\t"
                f"{proxy_power:.3f}\t{mean_diff:.4f}"
            )


if __name__ == "__main__":
    main()
