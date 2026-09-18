import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def test_benchmark_registry_schema_and_example():
    schema = json.loads((DATA / "benchmark_cases.schema.json").read_text(encoding="utf-8"))
    example = json.loads((DATA / "benchmark_cases.example.json").read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema, format_checker=FormatChecker()).validate(example)


def test_track_a_example_excludes_post_cutoff_outcome_source():
    cases = json.loads((DATA / "benchmark_cases.example.json").read_text(encoding="utf-8"))
    case = cases[0]
    forbidden = [x for x in case["feature_sources"] if not x["track_a_allowed"]]
    assert forbidden
    assert all(x["first_public_at"] > case["source_cutoff"] for x in forbidden if x["first_public_at"])
    assert case["leakage_audit"]["future_outcome_sources_excluded"] is True
