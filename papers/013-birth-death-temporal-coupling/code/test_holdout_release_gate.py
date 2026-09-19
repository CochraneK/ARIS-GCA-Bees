import unittest

import holdout_release_gate as gate


class HoldoutGateTest(unittest.TestCase):
    def base(self):
        return {
            "schema_version": 1,
            "released": True,
            "pilot1_lock_version": "v2",
            "discovery_years": [1988, 1996],
            "holdout_years": [1997, 2005],
            "pilot1_lock_blob_sha": "a" * 40,
            "discovery_result_path": "results/discovery.json",
            "discovery_result_blob_sha": "b" * 40,
            "discovery_commit_sha": "c" * 40,
            "release_decision_commit_sha": "d" * 40,
        }

    def test_locked_by_default(self):
        obj = self.base()
        obj["released"] = False
        with self.assertRaises(gate.HoldoutLocked):
            gate.validate_manifest_dict(obj)

    def test_year_change_is_rejected(self):
        obj = self.base()
        obj["holdout_years"] = [1996, 2005]
        with self.assertRaises(gate.HoldoutLocked):
            gate.validate_manifest_dict(obj)

    def test_complete_manifest_schema_passes_static_check(self):
        gate.validate_manifest_dict(self.base())


if __name__ == "__main__":
    unittest.main()
