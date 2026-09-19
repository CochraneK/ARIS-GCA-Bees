#!/usr/bin/env python3
"""Gate H3/H4 execution until the traditional feature schema is frozen."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

LOCKED_EXIT = 2


def validate_schema(obj: dict) -> None:
    if obj.get("schema_version") != 1:
        raise ValueError("unsupported schema version")
    if obj.get("frozen") is not True:
        raise RuntimeError("traditional feature schema is not frozen")
    if not obj.get("implementation_blob_sha"):
        raise RuntimeError("missing frozen implementation blob")
    if not obj.get("test_vectors_blob_sha"):
        raise RuntimeError("missing frozen test-vector blob")
    if not obj.get("pseudo_generator_blob_sha"):
        raise RuntimeError("missing frozen pseudo-system generator blob")
    if obj.get("outcome_access_status") != "frozen-before-H3H4-outcomes":
        raise RuntimeError("outcome-access status is not pre-outcome frozen")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--schema",
        type=Path,
        default=Path(
            "papers/013-birth-death-temporal-coupling/process/"
            "TRADITIONAL_FEATURE_SCHEMA.json"
        ),
    )
    args = ap.parse_args()
    obj = json.loads(args.schema.read_text(encoding="utf-8"))
    try:
        validate_schema(obj)
    except (ValueError, RuntimeError) as exc:
        print(f"TRADITIONAL_FEATURES_LOCKED: {exc}")
        return LOCKED_EXIT
    print("TRADITIONAL_FEATURES_RELEASED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
