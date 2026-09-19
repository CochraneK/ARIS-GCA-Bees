import unittest

import traditional_model_gate as gate


class TraditionalModelGateTest(unittest.TestCase):
    def valid(self):
        return {
            "schema_version": 1,
            "frozen": True,
            "required_feature_freeze_version": "v1.0",
            "outcome_access_status": "model-frozen-before-H3H4-outcomes",
            "analysis_plan_path": "plan.md",
            "analysis_plan_blob_sha": "a" * 40,
            "analysis_code_path": "analysis.py",
            "analysis_code_blob_sha": "b" * 40,
        }

    def test_draft_model_is_locked(self):
        obj = self.valid()
        obj["frozen"] = False
        with self.assertRaises(gate.ModelLocked):
            gate.validate_model_schema(obj)

    def test_missing_analysis_code_hash_is_locked(self):
        obj = self.valid()
        obj["analysis_code_blob_sha"] = ""
        with self.assertRaises(gate.ModelLocked):
            gate.validate_model_schema(obj)

    def test_complete_static_model_schema_passes(self):
        gate.validate_model_schema(self.valid())


if __name__ == "__main__":
    unittest.main()
