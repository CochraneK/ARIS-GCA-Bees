#!/usr/bin/env python3
"""Mechanical release gate for the ARIS4C013 temporal holdout."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

LOCKED_EXIT = 2
EXPECTED_SPEC_VERSION = "v2"
EXPECTED_DISCOVERY_YEARS = [1988, 1996]
EXPECTED_HOLDOUT_YEARS = [1997, 2005]


class HoldoutLocked(RuntimeError):
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


def validate_manifest_dict(obj: dict) -> None:
    if obj.get("schema_version") != 1:
        raise HoldoutLocked("unsupported release-manifest schema")
    if obj.get("pilot1_lock_version") != EXPECTED_SPEC_VERSION:
        raise HoldoutLocked("Pilot 1 lock version is not v2")
    if obj.get("discovery_years") != EXPECTED_DISCOVERY_YEARS:
        raise HoldoutLocked("discovery years changed")
    if obj.get("holdout_years") != EXPECTED_HOLDOUT_YEARS:
        raise HoldoutLocked("holdout years changed")
    if obj.get("released") is not True:
        raise HoldoutLocked("holdout is intentionally locked")
    required = [
        "pilot1_lock_blob_sha",
        "discovery_result_path",
        "discovery_result_blob_sha",
        "discovery_commit_sha",
        "release_decision_commit_sha",
    ]
    missing = [k for k in required if not obj.get(k)]
    if missing:
        raise HoldoutLocked(
            "release manifest is incomplete: " + ", ".join(missing)
        )


def validate_repository_release(
    manifest_path: Path,
    repo_root: Path | None = None,
) -> dict:
    manifest_path = manifest_path.resolve()
    if repo_root is None:
        repo_root = Path(
            run_git(manifest_path.parent, "rev-parse", "--show-toplevel")
        )
    repo_root = repo_root.resolve()
    obj = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_manifest_dict(obj)

    lock_path = (
        repo_root
        / "papers/013-birth-death-temporal-coupling/process/"
        "PILOT1_DISCOVERY_LOCK.md"
    )
    current_lock_blob = run_git(
        repo_root, "hash-object", str(lock_path.relative_to(repo_root))
    )
    if current_lock_blob != obj["pilot1_lock_blob_sha"]:
        raise HoldoutLocked(
            "Pilot 1 lock content differs from the frozen release manifest"
        )

    result_rel = Path(obj["discovery_result_path"])
    if result_rel.is_absolute() or ".." in result_rel.parts:
        raise HoldoutLocked("discovery_result_path must be repo-relative")
    result_path = repo_root / result_rel
    if not result_path.is_file():
        raise HoldoutLocked("committed discovery result is missing")

    run_git(repo_root, "ls-files", "--error-unmatch", str(result_rel))
    current_result_blob = run_git(
        repo_root, "hash-object", str(result_rel)
    )
    if current_result_blob != obj["discovery_result_blob_sha"]:
        raise HoldoutLocked("discovery result blob does not match release")

    discovery_commit = obj["discovery_commit_sha"]
    release_commit = obj["release_decision_commit_sha"]
    for sha, label in (
        (discovery_commit, "discovery commit"),
        (release_commit, "release decision commit"),
    ):
        try:
            run_git(repo_root, "merge-base", "--is-ancestor", sha, "HEAD")
        except subprocess.CalledProcessError as exc:
            raise HoldoutLocked(
                f"{label} is not an ancestor of current HEAD"
            ) from exc

    try:
        run_git(
            repo_root,
            "merge-base",
            "--is-ancestor",
            discovery_commit,
            release_commit,
        )
    except subprocess.CalledProcessError as exc:
        raise HoldoutLocked(
            "release decision must be committed after discovery freeze"
        ) from exc

    decision_rel = (
        "papers/013-birth-death-temporal-coupling/process/"
        "HOLDOUT_RELEASE_DECISION.json"
    )
    try:
        decision_text = run_git(
            repo_root,
            "show",
            f"{release_commit}:{decision_rel}",
        )
        decision = json.loads(decision_text)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise HoldoutLocked(
            "release decision commit lacks a valid decision record"
        ) from exc

    if decision.get("authorized") is not True:
        raise HoldoutLocked("release decision is not authorized")
    if decision.get("pilot1_lock_version") != EXPECTED_SPEC_VERSION:
        raise HoldoutLocked("release decision does not bind Pilot 1 v2")
    if decision.get("pilot1_lock_blob_sha") != obj["pilot1_lock_blob_sha"]:
        raise HoldoutLocked("release decision lock blob mismatch")
    if (
        decision.get("discovery_result_blob_sha")
        != obj["discovery_result_blob_sha"]
    ):
        raise HoldoutLocked("release decision discovery blob mismatch")
    if decision.get("holdout_years") != EXPECTED_HOLDOUT_YEARS:
        raise HoldoutLocked("release decision holdout years changed")

    frozen_at_discovery = run_git(
        repo_root,
        "rev-parse",
        f"{discovery_commit}:{result_rel.as_posix()}",
    )
    if frozen_at_discovery != obj["discovery_result_blob_sha"]:
        raise HoldoutLocked(
            "discovery result was not frozen at discovery_commit_sha"
        )

    return obj


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--manifest",
        type=Path,
        default=Path(
            "papers/013-birth-death-temporal-coupling/process/"
            "HOLDOUT_RELEASE.json"
        ),
    )
    args = ap.parse_args()
    try:
        obj = validate_repository_release(args.manifest)
    except HoldoutLocked as exc:
        print(f"HOLDOUT_LOCKED: {exc}")
        return LOCKED_EXIT

    print("HOLDOUT_RELEASED")
    print(
        json.dumps(
            {
                "discovery_commit_sha": obj["discovery_commit_sha"],
                "release_decision_commit_sha": obj[
                    "release_decision_commit_sha"
                ],
                "discovery_result_path": obj["discovery_result_path"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
