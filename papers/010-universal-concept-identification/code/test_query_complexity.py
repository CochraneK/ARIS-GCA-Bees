"""Unit tests for query_complexity.py.

Run from this directory:
    python -m unittest -v test_query_complexity.py
"""

import unittest

from query_complexity import (
    collision_groups,
    expected_greedy_cost,
    greedy_information_gain_query,
    greedy_path_costs,
    huffman_expected_length,
    max_targets,
    minimum_static_separating_set,
    unrestricted_uniform_binary_expected_cost,
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



    def test_unrestricted_uniform_huffman_baseline(self):
        self.assertAlmostEqual(
            unrestricted_uniform_binary_expected_cost(15),
            59 / 15,
        )
        self.assertAlmostEqual(
            huffman_expected_length([0.5, 0.25, 0.25]),
            1.5,
        )

    def test_greedy_binary_demo_matches_optimal_expected_cost(self):
        matrix = demo_matrix()
        self.assertAlmostEqual(expected_greedy_cost(matrix), 11 / 3)
        self.assertEqual(max(greedy_path_costs(matrix)), 4.0)

    def test_greedy_supports_multivalued_answers(self):
        matrix = [
            ["YES", "A"],
            ["NO", "A"],
            ["UNKNOWN", "B"],
            ["UNDEFINED", "B"],
        ]
        first = greedy_information_gain_query(
            matrix,
            candidates=[0, 1, 2, 3],
            query_indices=[0, 1],
        )
        self.assertEqual(first, 0)
        self.assertEqual(greedy_path_costs(matrix), [1.0, 1.0, 1.0, 1.0])

    def test_cost_sensitive_greedy_can_change_first_query(self):
        matrix = [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
        ]
        self.assertEqual(
            greedy_information_gain_query(matrix, [0, 1, 2, 3], [0, 1]),
            0,
        )
        self.assertEqual(
            greedy_information_gain_query(
                matrix,
                [0, 1, 2, 3],
                [0, 1],
                query_costs=[10.0, 1.0],
            ),
            1,
        )


if __name__ == "__main__":
    unittest.main()
