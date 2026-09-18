#!/usr/bin/env python3
"""Reference utilities for ARIS4C009's multi-objective fidelity frontier.

This module is methodological scaffolding. It does not contain empirical patient data
and must not be presented as evidence for the ARIS4C009 hypotheses.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Representation:
    name: str
    # All fidelity/utility entries are oriented so higher is better.
    fidelity: tuple[float, ...]
    validity: tuple[float, ...]
    prediction: tuple[float, ...]
    # All burden entries are oriented so lower is better.
    burden: tuple[float, ...]


def _all_geq(a: Sequence[float], b: Sequence[float], tol: float = 1e-12) -> bool:
    return all(x + tol >= y for x, y in zip(a, b))


def _all_leq(a: Sequence[float], b: Sequence[float], tol: float = 1e-12) -> bool:
    return all(x <= y + tol for x, y in zip(a, b))


def _any_gt(a: Sequence[float], b: Sequence[float], tol: float = 1e-12) -> bool:
    return any(x > y + tol for x, y in zip(a, b))


def _any_lt(a: Sequence[float], b: Sequence[float], tol: float = 1e-12) -> bool:
    return any(x + tol < y for x, y in zip(a, b))


def dominates(a: Representation, b: Representation) -> bool:
    """Return True if representation a Pareto-dominates b."""
    weakly_better = (
        _all_geq(a.fidelity, b.fidelity)
        and _all_geq(a.validity, b.validity)
        and _all_geq(a.prediction, b.prediction)
        and _all_leq(a.burden, b.burden)
    )
    strictly_better = (
        _any_gt(a.fidelity, b.fidelity)
        or _any_gt(a.validity, b.validity)
        or _any_gt(a.prediction, b.prediction)
        or _any_lt(a.burden, b.burden)
    )
    return weakly_better and strictly_better


def pareto_frontier(items: Iterable[Representation]) -> list[Representation]:
    """Return non-dominated representations."""
    items = list(items)
    return [
        item
        for item in items
        if not any(dominates(other, item) for other in items if other is not item)
    ]


def semantic_fidelity(source_answers: Sequence[object], repr_answers: Sequence[object]) -> float:
    """Exact-agreement semantic fidelity for categorical benchmark questions."""
    if len(source_answers) != len(repr_answers):
        raise ValueError("Answer vectors must have equal length.")
    if not source_answers:
        raise ValueError("At least one benchmark question is required.")
    return sum(a == b for a, b in zip(source_answers, repr_answers)) / len(source_answers)


def relation_f1(
    source_edges: set[tuple[str, str, str]],
    repr_edges: set[tuple[str, str, str]],
) -> float:
    """Relation-level F1 for labeled phenomenological graph edges."""
    if not source_edges and not repr_edges:
        return 1.0
    if not source_edges or not repr_edges:
        return 0.0
    tp = len(source_edges & repr_edges)
    precision = tp / len(repr_edges)
    recall = tp / len(source_edges)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def context_loss(loss_with_context: float, loss_without_context: float) -> float:
    """Incremental interpretation loss caused by removing context."""
    return loss_without_context - loss_with_context


if __name__ == "__main__":
    # Synthetic engineering example only.
    demo = [
        Representation(
            "rich_interview",
            fidelity=(0.98, 0.96, 0.95),
            validity=(0.75,),
            prediction=(0.72,),
            burden=(0.95, 0.90),
        ),
        Representation(
            "structured_phenomenology",
            fidelity=(0.91, 0.89, 0.86),
            validity=(0.80,),
            prediction=(0.78,),
            burden=(0.55, 0.60),
        ),
        Representation(
            "brief_scale",
            fidelity=(0.61, 0.45, 0.42),
            validity=(0.70,),
            prediction=(0.73,),
            burden=(0.10, 0.12),
        ),
    ]

    print("Synthetic Pareto frontier:")
    for item in pareto_frontier(demo):
        print(f"- {item.name}")
