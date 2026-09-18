"""Core combinatorial utilities for ARIS4C010.

This module intentionally contains no semantic data. It verifies the mathematical
plumbing used by later concept-question benchmarks: finite-channel bounds,
signature collisions, minimum static separating bases for small instances, and
exact optimal adaptive trees for small deterministic response matrices.
"""

from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from math import ceil, log2
from typing import Hashable, Iterable, Sequence


def entropy_bits(probabilities: Iterable[float]) -> float:
    """Shannon entropy in bits."""
    return -sum(p * log2(p) for p in probabilities if p > 0)


def max_targets(question_budget: int, response_count: int = 2) -> int:
    """Maximum leaves in a full response_count-ary tree of given depth."""
    if question_budget < 0:
        raise ValueError("question_budget must be nonnegative")
    if response_count < 2:
        raise ValueError("response_count must be at least 2")
    return response_count ** question_budget


def worst_case_lower_bound(candidate_count: int, response_count: int = 2) -> int:
    """Information-theoretic lower bound on worst-case question depth."""
    if candidate_count < 0:
        raise ValueError("candidate_count must be nonnegative")
    if response_count < 2:
        raise ValueError("response_count must be at least 2")
    if candidate_count <= 1:
        return 0
    return ceil(log2(candidate_count) / log2(response_count))


def signatures(
    matrix: Sequence[Sequence[Hashable]],
    query_indices: Iterable[int] | None = None,
) -> list[tuple[Hashable, ...]]:
    """Return each candidate's response signature on selected queries."""
    if not matrix:
        return []
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("response matrix must be rectangular")
    qs = tuple(range(width) if query_indices is None else query_indices)
    return [tuple(row[j] for j in qs) for row in matrix]


def collision_groups(
    matrix: Sequence[Sequence[Hashable]],
    query_indices: Iterable[int] | None = None,
) -> list[list[int]]:
    """Candidate-index groups that remain indistinguishable."""
    groups: dict[tuple[Hashable, ...], list[int]] = {}
    for i, signature in enumerate(signatures(matrix, query_indices)):
        groups.setdefault(signature, []).append(i)
    return [group for group in groups.values() if len(group) > 1]


def is_separating(
    matrix: Sequence[Sequence[Hashable]],
    query_indices: Iterable[int] | None = None,
) -> bool:
    """Whether selected queries uniquely identify every row/candidate."""
    sigs = signatures(matrix, query_indices)
    return len(sigs) == len(set(sigs))


def minimum_static_separating_set(
    matrix: Sequence[Sequence[Hashable]],
) -> tuple[int, ...] | None:
    """Exact minimum separating query subset for small matrices.

    Brute force by design. Later large benchmarks should use ILP/CP-SAT,
    greedy Test-Cover approximations, or specialized solvers.
    """
    if not matrix:
        return tuple()
    width = len(matrix[0])
    n = len(matrix)
    if n <= 1:
        return tuple()
    for k in range(width + 1):
        for qs in combinations(range(width), k):
            if is_separating(matrix, qs):
                return qs
    return None


def optimal_tree_cost(
    matrix: Sequence[Sequence[Hashable]],
    probabilities: Sequence[float] | None = None,
    objective: str = "expected",
) -> tuple[float, int | None]:
    """Exact optimal adaptive tree cost for a small deterministic matrix.

    Returns (cost, first_query_index). Unit query costs are assumed.
    objective: "expected" or "worst".
    """
    if objective not in {"expected", "worst"}:
        raise ValueError("objective must be 'expected' or 'worst'")
    if not matrix:
        return 0.0, None

    n = len(matrix)
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("response matrix must be rectangular")

    if probabilities is None:
        probabilities = [1.0 / n] * n
    if len(probabilities) != n or any(p < 0 for p in probabilities):
        raise ValueError("invalid probabilities")
    total = sum(probabilities)
    if total <= 0:
        raise ValueError("probabilities must have positive total mass")

    probs = tuple(p / total for p in probabilities)
    frozen = tuple(tuple(row) for row in matrix)

    @lru_cache(maxsize=None)
    def solve(
        candidates: tuple[int, ...],
        queries: tuple[int, ...],
    ) -> tuple[float, int | None]:
        if len(candidates) <= 1:
            return 0.0, None

        candidate_mass = sum(probs[i] for i in candidates)
        best_cost = float("inf")
        best_query = None

        for q in queries:
            partitions: dict[Hashable, list[int]] = {}
            for i in candidates:
                partitions.setdefault(frozen[i][q], []).append(i)
            if len(partitions) <= 1:
                continue

            remaining = tuple(x for x in queries if x != q)
            branch_costs: list[tuple[float, float]] = []
            for part in partitions.values():
                part_tuple = tuple(part)
                subcost, _ = solve(part_tuple, remaining)
                weight = sum(probs[i] for i in part_tuple) / candidate_mass
                branch_costs.append((weight, subcost))

            if objective == "expected":
                cost = 1.0 + sum(weight * subcost for weight, subcost in branch_costs)
            else:
                cost = 1.0 + max(subcost for _, subcost in branch_costs)

            if cost < best_cost:
                best_cost = cost
                best_query = q

        return best_cost, best_query

    return solve(tuple(range(n)), tuple(range(width)))


def _sanity_demo() -> None:
    # Twelve synthetic candidates encoded by four useful binary tests plus
    # two redundant tests. This is a code check, not semantic evidence.
    matrix: list[list[int]] = []
    for i in range(12):
        bits = [(i >> bit) & 1 for bit in range(4)]
        matrix.append(bits + [bits[0], bits[1] ^ bits[2]])

    print(f"20 binary questions: {max_targets(20):,} leaves")
    print(f"21 binary questions: {max_targets(21):,} leaves")
    print(
        "12-candidate binary lower bound:",
        worst_case_lower_bound(12),
        "questions",
    )
    print("minimum static separating queries:", minimum_static_separating_set(matrix))
    print("optimal worst-case tree:", optimal_tree_cost(matrix, objective="worst"))
    print("optimal expected tree:", optimal_tree_cost(matrix, objective="expected"))
    print("collisions if one essential bit is omitted:", collision_groups(matrix, [0, 1, 2]))


if __name__ == "__main__":
    _sanity_demo()
