"""Pilot 2: source-derived OEWN lexical-sense identification.

Targets are real OEWN senses. Semantic YES/NO mappings are exploratory and
machine_mapped_unreviewed. This script separates source-native lexname
separation from the added semantic-query family.

Run from this directory:
    python pilot2_oewn_lexical.py
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from query_complexity import (
    collision_groups,
    greedy_path_costs,
    minimum_static_separating_set,
    optimal_tree_cost,
    unrestricted_uniform_binary_expected_cost,
    worst_case_lower_bound,
)

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data" / "pilot2"


def pairwise_separation_coverage(matrix):
    n = len(matrix)
    if n <= 1:
        return 1.0
    separated = 0
    total = n * (n - 1) // 2
    for i in range(n):
        for j in range(i + 1, n):
            if tuple(matrix[i]) != tuple(matrix[j]):
                separated += 1
    return separated / total


def main():
    targets_pkg = json.loads((DATA / "oewn_senses.v0.json").read_text(encoding="utf-8"))
    query_pkg = json.loads((DATA / "semantic_queries.v0.json").read_text(encoding="utf-8"))

    records = targets_pkg["records"]
    target_ids = [row["target_id"] for row in records]
    lexnames = [row["source_assertions"]["lexname"] for row in records]
    lexname_vocab = sorted(set(lexnames))

    lex_matrix = [
        [int(lexname == category) for category in lexname_vocab]
        for lexname in lexnames
    ]

    query_ids = [q["query_id"] for q in query_pkg["queries"]]
    feature_names = [qid.removeprefix("p2-") for qid in query_ids]
    yes_map = query_pkg["target_yes_features"]

    sem_matrix = []
    for target_id in target_ids:
        yes = set(yes_map[target_id])
        sem_matrix.append([int(name in yes) for name in feature_names])

    lex_collisions = [
        [target_ids[i] for i in group]
        for group in collision_groups(lex_matrix)
    ]
    sem_collisions = [
        [target_ids[i] for i in group]
        for group in collision_groups(sem_matrix)
    ]

    min_basis = minimum_static_separating_set(sem_matrix)
    if min_basis is None:
        min_basis_names = None
    else:
        min_basis_names = [feature_names[i] for i in min_basis]

    exact_expected, first_q_expected = optimal_tree_cost(
        sem_matrix,
        objective="expected",
    )
    exact_worst, first_q_worst = optimal_tree_cost(
        sem_matrix,
        objective="worst",
    )
    greedy_costs = greedy_path_costs(sem_matrix)

    n = len(target_ids)
    unrestricted_expected = unrestricted_uniform_binary_expected_cost(n)
    unrestricted_worst = worst_case_lower_bound(n)

    results = {
        "targets": n,
        "lexname_categories": len(lexname_vocab),
        "lexname_collision_groups": lex_collisions,
        "lexname_pairwise_separation_coverage": pairwise_separation_coverage(lex_matrix),
        "semantic_queries": len(feature_names),
        "semantic_collision_groups": sem_collisions,
        "semantic_pairwise_separation_coverage": pairwise_separation_coverage(sem_matrix),
        "minimum_static_semantic_basis_size": None if min_basis is None else len(min_basis),
        "minimum_static_semantic_basis": min_basis_names,
        "semantic_optimal_expected_questions": exact_expected,
        "semantic_optimal_worst_questions": exact_worst,
        "semantic_optimal_first_query_expected": None if first_q_expected is None else feature_names[first_q_expected],
        "semantic_optimal_first_query_worst": None if first_q_worst is None else feature_names[first_q_worst],
        "greedy_path_costs": dict(zip(target_ids, greedy_costs)),
        "unrestricted_optimal_expected_questions": unrestricted_expected,
        "unrestricted_optimal_worst_questions": unrestricted_worst,
        "semantic_query_overhead_expected": exact_expected - unrestricted_expected,
        "semantic_query_overhead_worst": exact_worst - unrestricted_worst,
    }

    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
