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
from heapq import heapify, heappop, heappush
from typing import Hashable, Iterable, Sequence


def entropy_bits(probabilities: Iterable[float]) -> float:
    """Shannon entropy in bits."""
    return -sum(p * log2(p) for p in probabilities if p > 0)



def huffman_expected_length(probabilities: Iterable[float]) -> float:
    """Optimal expected binary prefix-code length for a target prior.

    This is the unrestricted binary-message baseline when arbitrary partitions
    are allowed and every question has unit cost.
    """
    probs = [float(p) for p in probabilities if p > 0]
    if not probs:
        return 0.0
    total = sum(probs)
    if total <= 0:
        raise ValueError("probabilities must have positive total mass")
    heap = [p / total for p in probs]
    if len(heap) == 1:
        return 0.0
    heapify(heap)
    cost = 0.0
    while len(heap) > 1:
        a = heappop(heap)
        b = heappop(heap)
        merged = a + b
        cost += merged
        heappush(heap, merged)
    return cost


def unrestricted_uniform_binary_expected_cost(candidate_count: int) -> float:
    """Optimal expected unrestricted binary questions for a uniform prior."""
    if candidate_count < 0:
        raise ValueError("candidate_count must be nonnegative")
    if candidate_count <= 1:
        return 0.0
    return huffman_expected_length([1.0] * candidate_count)


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



def response_entropy(
    matrix: Sequence[Sequence[Hashable]],
    candidates: Sequence[int],
    query_index: int,
    probabilities: Sequence[float] | None = None,
) -> float:
    """Entropy of one query's response distribution on a candidate subset."""
    if not candidates:
        return 0.0
    n = len(matrix)
    if probabilities is None:
        probabilities = [1.0 / n] * n
    total = sum(probabilities[i] for i in candidates)
    if total <= 0:
        raise ValueError("candidate probability mass must be positive")
    masses: dict[Hashable, float] = {}
    for i in candidates:
        answer = matrix[i][query_index]
        masses[answer] = masses.get(answer, 0.0) + probabilities[i] / total
    return entropy_bits(masses.values())


def greedy_information_gain_query(
    matrix: Sequence[Sequence[Hashable]],
    candidates: Sequence[int],
    query_indices: Sequence[int],
    probabilities: Sequence[float] | None = None,
    query_costs: Sequence[float] | None = None,
) -> int | None:
    """Pick the query maximizing response entropy per unit cost.

    For a deterministic response matrix, expected information gain from a query
    equals the entropy of its response distribution conditional on the current
    candidate set.
    """
    if not candidates or not query_indices:
        return None
    width = len(matrix[0]) if matrix else 0
    if query_costs is None:
        query_costs = [1.0] * width
    if len(query_costs) != width:
        raise ValueError("query_costs must match matrix width")
    if any(cost <= 0 for cost in query_costs):
        raise ValueError("query costs must be positive")

    best_query = None
    best_score = -1.0
    for q in query_indices:
        partitions = {matrix[i][q] for i in candidates}
        if len(partitions) <= 1:
            continue
        gain = response_entropy(matrix, candidates, q, probabilities)
        score = gain / query_costs[q]
        if score > best_score:
            best_score = score
            best_query = q
    return best_query


def greedy_path_costs(
    matrix: Sequence[Sequence[Hashable]],
    probabilities: Sequence[float] | None = None,
    query_costs: Sequence[float] | None = None,
) -> list[float]:
    """Simulate cost-sensitive greedy information gain for every target.

    If the admissible query family cannot separate the remaining candidates,
    unresolved targets receive float("inf").
    """
    if not matrix:
        return []
    n = len(matrix)
    width = len(matrix[0])
    if any(len(row) != width for row in matrix):
        raise ValueError("response matrix must be rectangular")
    if probabilities is None:
        probabilities = [1.0 / n] * n
    if query_costs is None:
        query_costs = [1.0] * width
    if len(probabilities) != n:
        raise ValueError("probabilities must match candidate count")
    if len(query_costs) != width:
        raise ValueError("query_costs must match matrix width")

    costs: list[float] = []
    for target in range(n):
        candidates = list(range(n))
        remaining = list(range(width))
        spent = 0.0

        while len(candidates) > 1:
            q = greedy_information_gain_query(
                matrix,
                candidates,
                remaining,
                probabilities,
                query_costs,
            )
            if q is None:
                spent = float("inf")
                break
            spent += query_costs[q]
            answer = matrix[target][q]
            candidates = [i for i in candidates if matrix[i][q] == answer]
            remaining.remove(q)

        costs.append(spent)
    return costs


def expected_greedy_cost(
    matrix: Sequence[Sequence[Hashable]],
    probabilities: Sequence[float] | None = None,
    query_costs: Sequence[float] | None = None,
) -> float:
    """Expected greedy path cost under a target prior."""
    if not matrix:
        return 0.0
    n = len(matrix)
    if probabilities is None:
        probabilities = [1.0 / n] * n
    total = sum(probabilities)
    if total <= 0:
        raise ValueError("probabilities must have positive mass")
    normalized = [p / total for p in probabilities]
    path_costs = greedy_path_costs(matrix, normalized, query_costs)
    if any(cost == float("inf") and p > 0 for cost, p in zip(path_costs, normalized)):
        return float("inf")
    return sum(p * cost for p, cost in zip(normalized, path_costs))


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
