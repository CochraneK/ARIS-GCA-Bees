#!/usr/bin/env python3
"""Export the frozen ARIS4C016 coding sample to a PRIVATE local CSV.

IMPORTANT: the generated sheet contains raw taboo expressions/translations and
must not be committed to the public repository. By default this script refuses
to write anywhere inside the ARIS4C repository tree.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

GUID = "8nyga"
VIEW_ONLY = "60b964248cc64a8793a9013075132a1c"
SHA256 = "c725a30913e604e8344f4990c8d63990dcf0271e3a65765ddc3fa591b8cb1387"
EXPECTED_MANIFEST_SHA256 = "48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4"
EXPECTED_N = 300


def download_source() -> list[dict[str, str]]:
    url = f"https://osf.io/download/{GUID}/?view_only={VIEW_ONLY}"
    with urllib.request.urlopen(url, timeout=120) as response:
        blob = response.read()
    digest = hashlib.sha256(blob).hexdigest()
    if digest != SHA256:
        raise RuntimeError(f"Study-1 checksum mismatch: {digest}")
    return list(csv.DictReader(io.StringIO(blob.decode("utf-8-sig", errors="replace"))))


def frozen_sample() -> dict:
    sampler = Path(__file__).with_name("build_audit_sample.py")
    proc = subprocess.run(
        [sys.executable, str(sampler)],
        check=True,
        capture_output=True,
        text=True,
        timeout=180,
    )
    payload = json.loads(proc.stdout)
    rows = payload.get("rows", [])
    if len(rows) != EXPECTED_N:
        raise RuntimeError(f"Expected {EXPECTED_N} frozen rows, got {len(rows)}")

    lines = ["sample,row_index,row_hash,stratum"]
    for row in sorted(rows, key=lambda r: (r["sample"], int(r["row_index"]))):
        lines.append(
            f'{row["sample"]},{row["row_index"]},{row["row_hash"]},'
            f'{row.get("selection_stratum", "backfill")}'
        )
    manifest = "\n".join(lines) + "\n"
    digest = hashlib.sha256(manifest.encode("utf-8")).hexdigest()
    if digest != EXPECTED_MANIFEST_SHA256:
        raise RuntimeError(
            "Frozen-sample manifest mismatch. "
            f"Expected {EXPECTED_MANIFEST_SHA256}, got {digest}"
        )
    return payload


def is_within(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Private CSV output path")
    parser.add_argument(
        "--unsafe-allow-repo-output",
        action="store_true",
        help="Override protection against writing raw taboo text inside repo.",
    )
    parser.add_argument("--coder-id", default="", help="Optional coder identifier")
    args = parser.parse_args()

    output = Path(args.output).expanduser().resolve()
    repo_root = Path(__file__).resolve().parents[3]

    if is_within(output, repo_root) and not args.unsafe_allow_repo_output:
        raise SystemExit(
            "REFUSED: private coding sheet contains raw taboo/slur text and "
            "must not be written inside the public ARIS4C repository. "
            "Choose a path outside the repo."
        )

    source = download_source()
    sample = frozen_sample()

    columns = [
        "row_hash",
        "sample",
        "source_row_index",
        "selection_stratum",
        "original_expression",
        "english_translation",
        "source_category1",
        "source_category2",
        "source_category3",
        "source_production_n",
        "semantic_source",
        "target",
        "pragmatic_function",
        "social_indexical_basis",
        "taboo_mechanism",
        "confidence",
        "native_review_required",
        "evidence_note",
        "coder_id",
    ]

    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for selected in sample["rows"]:
            idx = int(selected["row_index"])
            raw = source[idx - 1]
            if raw.get("lang") != selected["sample"]:
                raise RuntimeError(f"Sample mismatch at source row {idx}")
            writer.writerow({
                "row_hash": selected["row_hash"],
                "sample": selected["sample"],
                "source_row_index": idx,
                "selection_stratum": selected.get("selection_stratum", "backfill"),
                "original_expression": raw.get("word_clean", ""),
                "english_translation": raw.get("english_translation", ""),
                "source_category1": raw.get("category", ""),
                "source_category2": raw.get("category2", ""),
                "source_category3": raw.get("category3", ""),
                "source_production_n": raw.get("n", ""),
                "semantic_source": "",
                "target": "",
                "pragmatic_function": "",
                "social_indexical_basis": "",
                "taboo_mechanism": "",
                "confidence": "",
                "native_review_required": "",
                "evidence_note": "",
                "coder_id": args.coder_id,
            })

    print(f"Wrote {EXPECTED_N} private coding rows to: {output}")
    print("DO NOT commit this generated file to the public repository.")


if __name__ == "__main__":
    main()
