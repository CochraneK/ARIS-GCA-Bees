"""Synthetic semantic Pilot 1 for ARIS4C010.

This is a constructed sanity benchmark, NOT empirical semantic evidence.
It asks whether a single ontology-kind projection can separate a deliberately
heterogeneous concept set, then adds orthogonal semantic axes.

Run:
    python pilot1_semantic_seed.py
"""

from __future__ import annotations

from collections import defaultdict
from math import ceil, log2

from query_complexity import (
    expected_greedy_cost,
    greedy_path_costs,
)


TARGETS = [
    ("dog", {"ont": ["organism"], "exist": "actual", "boundary": "crisp", "context": "invariant", "path": "ordinary", "level": "concept", "logical": "primitive", "epistemic": "decidable"}),
    ("water", {"ont": ["substance"], "exist": "actual", "boundary": "crisp", "context": "invariant", "path": "ordinary", "level": "concept", "logical": "primitive", "epistemic": "decidable"}),
    ("running", {"ont": ["process"], "exist": "actual", "boundary": "crisp", "context": "invariant", "path": "ordinary", "level": "concept", "logical": "primitive", "epistemic": "decidable"}),
    ("red", {"ont": ["property"], "exist": "actual", "boundary": "scalar_context", "context": "invariant", "path": "ordinary", "level": "concept", "logical": "primitive", "epistemic": "decidable"}),
    ("teacher", {"ont": ["role", "social"], "exist": "actual", "boundary": "convention", "context": "social", "path": "ordinary", "level": "concept", "logical": "primitive", "epistemic": "decidable"}),
    ("justice", {"ont": ["social"], "exist": "actual", "boundary": "prototype", "context": "social", "path": "ordinary", "level": "concept", "logical": "primitive", "epistemic": "decidable"}),
    ("unicorn", {"ont": ["organism", "fictional"], "exist": "fictional", "boundary": "crisp", "context": "invariant", "path": "ordinary", "level": "concept", "logical": "primitive", "epistemic": "decidable"}),
    ("current_king_of_france", {"ont": ["role", "social"], "exist": "empty", "boundary": "crisp", "context": "temporal", "path": "presupposition_failure", "level": "referent", "logical": "relation", "epistemic": "decidable"}),
    ("round_square", {"ont": ["geometric"], "exist": "impossible", "boundary": "crisp", "context": "invariant", "path": "inconsistent", "level": "concept", "logical": "conjunction", "epistemic": "decidable"}),
    ("bank_financial_sense", {"ont": ["social"], "exist": "actual", "boundary": "convention", "context": "social", "path": "ordinary", "level": "sense", "logical": "primitive", "epistemic": "decidable"}),
    ("bank_river_sense", {"ont": ["region"], "exist": "actual", "boundary": "crisp", "context": "invariant", "path": "ordinary", "level": "sense", "logical": "primitive", "epistemic": "decidable"}),
    ("tall", {"ont": ["property"], "exist": "actual", "boundary": "vague", "context": "comparison", "path": "ordinary", "level": "concept", "logical": "primitive", "epistemic": "decidable"}),
    ("here", {"ont": ["other"], "exist": "actual", "boundary": "crisp", "context": "spatial", "path": "ordinary", "level": "sense", "logical": "primitive", "epistemic": "context_required"}),
    ("and", {"ont": ["logical"], "exist": "actual", "boundary": "crisp", "context": "invariant", "path": "ordinary", "level": "rule", "logical": "metalinguistic", "epistemic": "decidable"}),
    ("liar_sentence", {"ont": ["logical", "information"], "exist": "actual", "boundary": "crisp", "context": "invariant", "path": "liar_like", "level": "proposition", "logical": "higher_order", "epistemic": "decidable"}),
    ("halting_set", {"ont": ["set", "logical"], "exist": "actual", "boundary": "crisp", "context": "invariant", "path": "ordinary", "level": "concept", "logical": "higher_order", "epistemic": "undecidable"}),
]

ONTOLOGY_VALUES = [
    "organism", "substance", "process", "property", "role", "social",
    "fictional", "geometric", "region", "other", "logical", "information", "set",
]

ALL_QUERIES = (
    [("ont", value) for value in ONTOLOGY_VALUES]
    + [
        ("exist", "fictional"),
        ("exist", "empty"),
        ("exist", "impossible"),
        ("boundary", "vague"),
        ("boundary", "prototype"),
        ("boundary", "convention"),
        ("boundary", "scalar_context"),
        ("context", "temporal"),
        ("context", "comparison"),
        ("context", "spatial"),
        ("path", "presupposition_failure"),
        ("path", "inconsistent"),
        ("path", "liar_like"),
        ("level", "sense"),
        ("level", "referent"),
        ("level", "rule"),
        ("level", "proposition"),
        ("epistemic", "undecidable"),
        ("logical", "conjunction"),
        ("logical", "higher_order"),
        ("logical", "metalinguistic"),
    ]
)


def answer(features, query):
    field, value = query
    if field == "ont":
        return value in features[field]
    return features[field] == value


def response_matrix(queries):
    return [
        [answer(features, query) for query in queries]
        for _, features in TARGETS
    ]


def collisions(matrix):
    groups = defaultdict(list)
    for i, row in enumerate(matrix):
        groups[tuple(row)].append(TARGETS[i][0])
    return [group for group in groups.values() if len(group) > 1]


def greedy_static_cover(queries):
    """Greedy Test-Cover approximation over all target pairs."""
    unresolved = {
        (i, j)
        for i in range(len(TARGETS))
        for j in range(i + 1, len(TARGETS))
    }
    selected = []

    while unresolved:
        best_index = None
        best_cover = set()
        for qi, query in enumerate(queries):
            if qi in selected:
                continue
            cover = {
                (i, j)
                for i, j in unresolved
                if answer(TARGETS[i][1], query) != answer(TARGETS[j][1], query)
            }
            if len(cover) > len(best_cover):
                best_index = qi
                best_cover = cover

        if not best_cover:
            break

        selected.append(best_index)
        unresolved -= best_cover

    return selected, unresolved


def p6_coarsening_demo():
    rich = ["YES", "NO", "UNKNOWN", "UNDEFINED"]
    forced_binary = {
        "YES": "YES",
        "NO": "NO",
        "UNKNOWN": "NO",
        "UNDEFINED": "NO",
    }
    rich_unique = len(set(rich))
    binary_unique = len({forced_binary[x] for x in rich})
    return rich_unique, binary_unique


def main():
    taxonomy_queries = [("ont", value) for value in ONTOLOGY_VALUES]
    taxonomy_matrix = response_matrix(taxonomy_queries)

    selected, unresolved = greedy_static_cover(ALL_QUERIES)
    selected_queries = [ALL_QUERIES[i] for i in selected]
    selected_matrix = response_matrix(selected_queries)

    print("targets:", len(TARGETS))
    print("binary information lower bound:", ceil(log2(len(TARGETS))))
    print("taxonomy-only collisions:", collisions(taxonomy_matrix))
    print("greedy static semantic basis size:", len(selected_queries))
    print("greedy static semantic basis:", selected_queries)
    print("unresolved pairs after multi-axis basis:", len(unresolved))
    print("greedy adaptive path costs:", greedy_path_costs(selected_matrix))
    print("greedy adaptive expected cost:", expected_greedy_cost(selected_matrix))
    print("greedy adaptive worst-case cost:", max(greedy_path_costs(selected_matrix)))
    rich_unique, binary_unique = p6_coarsening_demo()
    print("P6 toy responses distinguish:", rich_unique, "states")
    print("forced binary coarsening distinguishes:", binary_unique, "states")


if __name__ == "__main__":
    main()
