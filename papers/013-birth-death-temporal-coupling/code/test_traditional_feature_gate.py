import unittest

import traditional_feature_gate as gate


class TraditionalFeatureGateTest(unittest.TestCase):
    def valid(self):
        return {
            "schema_version": 1,
            "frozen": True,
            "feature_freeze_version": "v1.0",
            "outcome_access_status": "feature-frozen-before-H3H4-outcomes",
            "dependency_pin": {
                "package": "lunar_python",
                "version": "1.4.8",
            },
            "implementation": {"path": "a.py", "blob_sha": "a" * 40},
            "test_vectors": {"path": "b.json", "blob_sha": "b" * 40},
            "pseudo_generator": {"path": "c.py", "blob_sha": "c" * 40},
        }

    def test_draft_is_locked(self):
        obj = self.valid()
        obj["frozen"] = False
        with self.assertRaises(gate.FeatureLocked):
            gate.validate_schema(obj)

    def test_dependency_change_is_locked(self):
        obj = self.valid()
        obj["dependency_pin"]["version"] = "9.9.9"
        with self.assertRaises(gate.FeatureLocked):
            gate.validate_schema(obj)

    def test_missing_blob_is_locked(self):
        obj = self.valid()
        obj["implementation"]["blob_sha"] = ""
        with self.assertRaises(gate.FeatureLocked):
            gate.validate_schema(obj)

    def test_complete_schema_passes_static_check(self):
        gate.validate_schema(self.valid())


if __name__ == "__main__":
    unittest.main()
