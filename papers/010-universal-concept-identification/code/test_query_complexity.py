"""Unit tests for query_complexity.py.

Run from this directory:
    python -m unittest -v test_query_complexity.py
"""

import unittest

from query_complexity import (
    collision_groups,
    max_targets,
    minimum_static_separating_set,
    optimal_tree_cost,
    worst_case_lower_bound,
)


def demo_matrix():
    rows = []
    for i in range(12):
        bits = [(i >> bit) & 1 for bit in range(4)]
        rows.append(bits + [bits[0], bits[1] ^ bits[2]])
    return rows


class QueryComplexityTests(unittest.TestCase):
    def test_twenty_question_capacity(self):
        self.assertEqual(max_targets(20), 1_048_576)
        self.assertEqual(max_targets(21), 2_097_152)

    def test_lower_bound(self):
        self.assertEqual(worst_case_lower_bound(12), 4)

    def test_minimum_static_basis(self):
        self.assertEqual(
            minimum_static_separating_set(demo_matrix()),
            (0, 1, 2, 3),
        )

    def test_optimal_tree(self):
        matrix = demo_matrix()
        worst, _ = optimal_tree_cost(matrix, objective="worst")
        expected, _ = optimal_tree_cost(matrix, objective="expected")
        self.assertEqual(worst, 4.0)
        self.assertAlmostEqual(expected, 11 / 3)

    def test_collision_detection(self):
        self.assertEqual(
            collision_groups(demo_matrix(), [0, 1, 2]),
            [[0, 8], [1, 9], [2, 10], [3, 11]],
        )


if __name__ == "__main__":
    unittest.main()
