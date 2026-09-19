#!/usr/bin/env python3
"""Verify the frozen ARIS4C013 traditional-feature layer.

Passing this gate authorizes deterministic FEATURE MATERIALIZATION only.
H3/H4 mortality outcome analysis is separately controlled by
traditional_model_gate.py.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

LOCKED_EXIT = 2
EXPECTED_FEATURE_VERSION = "v1.0"


class FeatureLocked(RuntimeError):
    pass


def run_git(repo_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def validate_schema(obj: dict) -> None:
    if obj.get("schema_version") != 1:
        raise FeatureLocked("unsupported schema version")
    if obj.get("frozen") is not True:
        raise FeatureLocked("traditional feature schema is not frozen")
    if obj.get("feature_freeze_version") != EXPECTED_FEATURE_VERSION:
        raise FeatureLocked("unexpected feature freeze version")
    if (
        obj.get("outcome_access_status")
        != "feature-frozen-before-H3H4-outcomes"
    ):
        raise FeatureLocked("feature freeze was not declared pre-outcome")
    pin = obj.get("dependency_pin") or {}
    if pin != {"package": "lunar_python", "version": "1.4.8"}:
        raise FeatureLocked("calendar dependency pin changed")
    for key in ("implementation", "test_vectors", "pseudo_generator"):
        item = obj.get(key) or {}
        if not item.get("path") or not item.get("blob_sha"):
            raise FeatureLocked(f"missing frozen {key} path/blob")


def validate_repository_freeze(
    schema_path: Path,
    repo_root: Path | None = None,
) -> dict:
    schema_path = schema_path.resolve()
    if repo_root is None:
        repo_root = Path(
            run_git(schema_path.parent, "rev-parse", "--show-toplevel")
        )
    repo_root = repo_root.resolve()
    obj = json.loads(schema_path.read_text(encoding="utf-8"))
    validate_schema(obj)

    for key in ("implementation", "test_vectors", "pseudo_generator"):
        item = obj[key]
        rel = Path(item["path"])
        if rel.is_absolute() or ".." in rel.parts:
            raise FeatureLocked(f"{key} path must be repo-relative")
        target = repo_root / rel
        if not target.is_file():
            raise FeatureLocked(f"{key} file is missing")
        run_git(repo_root, "ls-files", "--error-unmatch", rel.as_posix())
        actual = run_git(repo_root, "hash-object", rel.as_posix())
        if actual != item["blob_sha"]:
            raise FeatureLocked(
                f"{key} blob mismatch: expected {item['blob_sha']}, "
                f"found {actual}"
            )

    return obj


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
    try:
        obj = validate_repository_freeze(args.schema)
    except (FeatureLocked, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"TRADITIONAL_FEATURES_LOCKED: {exc}")
        return LOCKED_EXIT
    print(
        "TRADITIONAL_FEATURES_FROZEN "
        f"{obj['feature_freeze_version']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
