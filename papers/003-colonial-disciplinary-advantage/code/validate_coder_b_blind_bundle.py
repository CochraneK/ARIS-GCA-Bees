#!/usr/bin/env python3
"""Validate the ARIS4C003 Coder-B blind bundle."""

from __future__ import annotations

import csv
import hashlib
import io
import json
import re
from pathlib import Path

PAPER = Path(__file__).resolve().parents[1]
BLIND = PAPER / "process" / "coder_b_blind"
MANIFEST = BLIND / "MANIFEST.json"
EXPECTED_IDS = [f"D{i:02d}" for i in range(1, 22)]
EXPECTED_FILES = {
    "README.md",
    "WORKBUDDY_HANDOFF.md",
    "OUTPUT_TEMPLATE.md",
    "MANIFEST.json",
}


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def fail(msg: str) -> None:
    raise SystemExit(msg)


def main() -> None:
    if not MANIFEST.exists():
        fail(f"Missing blind manifest: {MANIFEST}")

    actual = {p.name for p in BLIND.iterdir() if p.is_file()}
    if actual != EXPECTED_FILES:
        fail(
            "Blind directory file set changed. "
            f"Expected={sorted(EXPECTED_FILES)} actual={sorted(actual)}"
        )

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if manifest.get("outcome_seen_when_built") is not False:
        fail("Blind manifest must state outcome_seen_when_built=false")
    policy = manifest.get("access_policy", {})
    if policy.get("mode") != "whitelist_only":
        fail("Blind manifest access policy must be whitelist_only")

    files = manifest.get("files", [])
    if len(files) != 3:
        fail(f"Expected 3 pinned blind-input files, got {len(files)}")

    allowed = set(policy.get("allowed_files", []))
    pinned = {str(x.get("path")) for x in files}
    if allowed != pinned:
        fail("Manifest allowed_files and pinned files differ")

    repo_root = PAPER.parents[1]
    for entry in files:
        rel = str(entry["path"])
        path = repo_root / rel
        if not path.exists():
            fail(f"Pinned blind file missing: {rel}")
        observed = git_blob_sha(path)
        if observed != entry.get("git_blob_sha"):
            fail(
                f"Blind input drifted without manifest update: {rel}; "
                f"expected {entry.get('git_blob_sha')} observed {observed}"
            )

    handoff = (BLIND / "WORKBUDDY_HANDOFF.md").read_text(encoding="utf-8")
    if "INDEPENDENCE_STATUS: PASS" not in handoff:
        fail("Handoff missing independence declaration contract")
    ids = re.findall(r"(?m)^\\| (D\\d{2}) \\|", handoff)
    if ids != EXPECTED_IDS:
        fail(f"Handoff frozen discipline table is not exactly D01-D21: {ids}")
    for d in range(1, 12):
        if f"**D{d} " not in handoff:
            fail(f"Handoff missing D{d} rubric dimension")

    banned_filenames = {
        "IKES_CODER_A.csv",
        "IKES_CODER_A.md",
        "IKES_FROZEN.csv",
        "IKES_CODER_B.csv",
        "IKES_CODER_B.md",
        "OPENALEX_SCHEMA_PROBE.json",
    }
    if actual.intersection(banned_filenames):
        fail(f"Prohibited artifact copied into blind bundle: {actual & banned_filenames}")

    template = (BLIND / "OUTPUT_TEMPLATE.md").read_text(encoding="utf-8")
    match = re.search(r"(?ims)```csv\\s*\\n(.*?)```", template)
    if not match:
        fail("Output template missing CSV block")
    rows = list(csv.reader(io.StringIO(match.group(1).strip())))
    if len(rows) != 22:
        fail(f"Output template should contain header + 21 rows, found {len(rows)}")
    if [r[0] for r in rows[1:]] != EXPECTED_IDS:
        fail("Output template concept order differs from D01-D21")
    for row in rows[1:]:
        if any(str(x).strip() for x in row[2:]):
            fail(f"Output template contains a prefilled score for {row[0]}")

    print(
        json.dumps(
            {
                "status": "PASS",
                "bundle": str(BLIND),
                "pinned_inputs": len(files),
                "concepts": len(EXPECTED_IDS),
                "outcome_seen": False,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
