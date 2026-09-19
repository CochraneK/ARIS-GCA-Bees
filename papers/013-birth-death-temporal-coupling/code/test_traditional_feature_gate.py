import unittest

import traditional_feature_gate as gate


class TraditionalFeatureGateTest(unittest.TestCase):
    def valid(self):
        return {
            "schema_version": 1,
            "frozen": True,
            "implementation_blob_sha": "a" * 40,
            "test_vectors_blob_sha": "b" * 40,
            "pseudo_generator_blob_sha": "c" * 40,
            "outcome_access_status": "frozen-before-H3H4-outcomes",
        }

    def test_draft_is_locked(self):
        obj = self.valid()
        obj["frozen"] = False
        with self.assertRaises(RuntimeError):
            gate.validate_schema(obj)

    def test_missing_hash_is_locked(self):
        obj = self.valid()
        obj["implementation_blob_sha"] = ""
        with self.assertRaises(RuntimeError):
            gate.validate_schema(obj)

    def test_complete_frozen_schema_passes(self):
        gate.validate_schema(self.valid())


if __name__ == "__main__":
    unittest.main()
