"""Evaluate arbitrary cutoff-safe feature scores against Pilot 1 outcomes.

Citation baselines in historical_backtest.py compute their score directly from
citation histories. Semantic/network ablations instead arrive as externally
computed score maps. This module gives them the *same* ranking evaluation
contract without letting future outcomes enter feature construction.

A score map is:
    paper_id -> numeric score

Higher score is assumed to mean higher rediscovery priority. If a feature has
the opposite direction (for example similarity where lower means more novel),
the caller must transform it explicitly and record that transformation.
"""

from __future__ import annotations

from typing import Mapping

from ranking_metrics import RankedItem, evaluate_ranking, ndcg_at_k


def build_items(
    scores: Mapping[str, float],
    relevance: Mapping[str, float],
) -> list[RankedItem]:
    """Join feature scores to future relevance by paper ID."""
    common = sorted(set(scores).intersection(relevance))
    return [
        RankedItem(
            paper_id=paper_id,
            score=float(scores[paper_id]),
            relevance=float(relevance[paper_id]),
        )
        for paper_id in common
    ]


def evaluate_score_map(
    scores: Mapping[str, float],
    *,
    relevance: Mapping[str, float],
    relevance_type: str,
    k: int,
    feature_name: str,
) -> dict[str, float | int | str]:
    """Evaluate one arbitrary score map using the standard Pilot 1 metrics."""
    if relevance_type not in {"binary", "graded"}:
        raise ValueError("relevance_type must be 'binary' or 'graded'")

    items = build_items(scores, relevance)
    if relevance_type == "binary":
        result = evaluate_ranking(items, k=k)
    else:
        result = {
            "n": len(items),
            "k": min(k, len(items)),
            "ndcg_at_k": ndcg_at_k(items, k) if items else 0.0,
        }

    return {
        "feature": feature_name,
        "relevance_type": relevance_type,
        **result,
    }


def evaluate_feature_outcome_matrix(
    feature_scores: Mapping[str, Mapping[str, float]],
    *,
    outcomes: Mapping[str, tuple[str, Mapping[str, float]]],
    k: int,
) -> dict[str, list[dict[str, float | int | str]]]:
    """Evaluate many external feature score maps against many outcomes."""
    result: dict[str, list[dict[str, float | int | str]]] = {}
    for outcome_name, (kind, relevance) in outcomes.items():
        result[outcome_name] = [
            evaluate_score_map(
                scores,
                relevance=relevance,
                relevance_type=kind,
                k=k,
                feature_name=feature_name,
            )
            for feature_name, scores in feature_scores.items()
        ]
    return result
