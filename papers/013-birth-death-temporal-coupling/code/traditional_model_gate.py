#!/usr/bin/env python3
"""Gate ARIS4C013 H3/H4 OUTCOME analysis.

Feature materialization may be frozen and reproducible while outcome analysis
remains locked. This separation prevents exploratory peeking simply because the
calendar conversion layer is ready.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from traditional_feature_gate import (
    FeatureLocked,
    validate_repository_freeze,
)

LOCKED_EXIT = 2


class ModelLocked(RuntimeError):
    pass


def validate_model_schema(obj: dict) -> None:
    if obj.get("schema_version") != 1:
        raise ModelLocked("unsupported model schema version")
    if obj.get("frozen") is not True:
        raise ModelLocked("traditional outcome model is not frozen")
    if obj.get("required_feature_freeze_version") != "v1.0":
        raise ModelLocked("unexpected required feature version")
    if (
        obj.get("outcome_access_status")
        != "model-frozen-before-H3H4-outcomes"
    ):
        raise ModelLocked("model was not declared frozen pre-outcome")
    for key in (
        "analysis_plan_path",
        "analysis_plan_blob_sha",
        "analysis_code_path",
        "analysis_code_blob_sha",
    ):
        if not obj.get(key):
            raise ModelLocked(f"missing {key}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--feature-schema",
        type=Path,
        default=Path(
            "papers/013-birth-death-temporal-coupling/process/"
            "TRADITIONAL_FEATURE_SCHEMA.json"
        ),
    )
    ap.add_argument(
        "--model-schema",
        type=Path,
        default=Path(
            "papers/013-birth-death-temporal-coupling/process/"
            "TRADITIONAL_MODEL_SCHEMA.json"
        ),
    )
    args = ap.parse_args()
    try:
        validate_repository_freeze(args.feature_schema)
        obj = json.loads(args.model_schema.read_text(encoding="utf-8"))
        validate_model_schema(obj)
    except (
        FeatureLocked,
        ModelLocked,
        ValueError,
        RuntimeError,
        json.JSONDecodeError,
    ) as exc:
        print(f"TRADITIONAL_MODEL_LOCKED: {exc}")
        return LOCKED_EXIT

    print("TRADITIONAL_MODEL_RELEASED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
