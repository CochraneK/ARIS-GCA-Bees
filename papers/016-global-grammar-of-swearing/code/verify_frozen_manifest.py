#!/usr/bin/env python3
"""Diagnose the ARIS4C016 frozen-manifest digest mismatch.

The freeze document (process/AUDIT_SAMPLE_FREEZE.md) declares the 300-row
public audit manifest SHA-256 to be EXPECTED_MANIFEST_SHA256. Regenerating the
manifest with the committed sampler against the checksum-verified OSF source
does not reproduce it. This script re-derives the digest deterministically,
searches a battery of plausible serialisations, and publishes partial digests so
that anyone still holding the original coding sheet can identify which
serialisation produced the frozen value.

Outputs row indices and hashes only; never emits a lexical item.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent
EXPECTED_MANIFEST_SHA256 = "48c58f91901e8c2a1aab01958e95ea28afaf0f33e7a98677f98e58b8a412c9b4"
EXPECTED_N = 300
# export_private_coding_sheet.py writes this header and labels unnamed strata "backfill".
EXPORTER_HEADER = "sample,row_index,row_hash,stratum"

LINE_ENDINGS = ("\n", "\r\n")
TRAILERS = ("newline", "none")


def regenerate_sampler_output() -> dict:
    proc = subprocess.run(
        [sys.executable, str(CODE / "build_audit_sample.py")],
        check=True,
        capture_output=True,
        text=True,
        timeout=300,
    )
    return json.loads(proc.stdout)


def exporter_manifest(rows: list[dict]) -> str:
    """Exactly the text export_private_coding_sheet.py hashes."""
    lines = [EXPORTER_HEADER]
    for r in sorted(rows, key=lambda r: (r["sample"], int(r["row_index"]))):
        lines.append(
            f'{r["sample"]},{r["row_index"]},{r["row_hash"]},{r.get("selection_stratum", "backfill")}'
        )
    return "\n".join(lines) + "\n"


def manifest_lines(rows: list[dict], header: tuple[str, ...]) -> list[str]:
    head = ",".join(header)
    body = []
    for r in rows:
        body.append(",".join(str(r.get(k, r.get("selection_stratum", "backfill"))) for k in header))
    return [head, *body]


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def serialisations(rows: list[dict]):
    """Yield (variant_id, manifest_text) over plausible manifest writings.

    Axes: row ordering, column set, header spelling, line ending, trailing
    newline, BOM, and whether the stratum column carries the sampler's field
    name. Combined, these cover the ways a freeze digest is usually computed by
    hand rather than by the exporter.
    """
    orderings = {
        "sorted_sample_rowindex": sorted(rows, key=lambda r: (r["sample"], int(r["row_index"]))),
        "sampler_order": rows,
        "sorted_rowindex": sorted(rows, key=lambda r: int(r["row_index"])),
        "sorted_rowhash": sorted(rows, key=lambda r: r["row_hash"]),
    }
    column_sets = {
        "sample_row_index_row_hash_stratum": ("sample", "row_index", "row_hash", "selection_stratum"),
        "sample_row_index_row_hash": ("sample", "row_index", "row_hash"),
        "row_index_row_hash": ("row_index", "row_hash"),
        "row_hash_only": ("row_hash",),
        "sample_row_index": ("sample", "row_index"),
    }
    for (oname, orows), (cname, cols) in itertools.product(orderings.items(), column_sets.items()):
        if cname == "sample_row_index_row_hash_stratum":
            lines = manifest_lines(orows, cols)
        else:
            lines = [",".join(cols), *[",".join(str(r.get(k, "")) for k in cols) for r in orows]]
        for le, trailer in itertools.product(LINE_ENDINGS, TRAILERS):
            body = le.join(lines) + (le if trailer == "newline" else "")
            yield f"{oname}|{cname}|eol={le!r}|{trailer}", body

    exporter = exporter_manifest(rows).rstrip("\n")
    for le, trailer in itertools.product(LINE_ENDINGS, TRAILERS):
        yield f"exporter_exact|eol={le!r}|{trailer}", le.join(exporter.split("\n")) + (
            le if trailer == "newline" else ""
        )

    # AUDIT_SAMPLE_FREEZE.md names the strata with hyphens; a freeze digest may
    # predate the field-name spelling used by the sampler.
    stratum_spellings = {
        "sampler_field": {},
        "freeze_doc_hyphen": {
            "missing_primary": "missing-primary-category",
            "unresolved": "unresolved-label",
            "multi_label": "multi-label",
            "random": "random",
            "backfill": "backfill",
        },
    }
    for sname, remap in stratum_spellings.items():
        remapped = [
            {**r, "selection_stratum": remap.get(r.get("selection_stratum", "backfill"), r.get("selection_stratum", "backfill"))}
            for r in rows
        ]
        text = exporter_manifest(remapped)
        yield f"exporter_exact|stratum={sname}", text


def partial_digests(rows: list[dict]) -> dict:
    """Digests a holder of the original sheet can compare against."""
    sorted_rows = sorted(rows, key=lambda r: (r["sample"], int(r["row_index"])))
    idx = digest("\n".join(f'{r["sample"]},{r["row_index"]}' for r in sorted_rows) + "\n")
    hashes = digest("\n".join(r["row_hash"] for r in sorted_rows) + "\n")
    pairs = digest("\n".join(f'{r["row_index"]},{r["row_hash"]}' for r in sorted_rows) + "\n")
    return {
        "sha256_of_sample_row_index_column_order": idx,
        "sha256_of_row_hash_column_only": hashes,
        "sha256_of_row_index_row_hash_pairs": pairs,
        "sha256_of_json_rows_canonical": digest(
            json.dumps(sorted_rows, sort_keys=True, separators=(",", ":"))
        ),
    }


def per_sample_digests(rows: list[dict]) -> dict:
    """Locate a divergence: digest of `row_index,row_hash` per community."""
    groups: dict[str, list[dict]] = {}
    for r in rows:
        groups.setdefault(r["sample"], []).append(r)
    return {
        sample: digest(
            "\n".join(
                f'{r["row_index"]},{r["row_hash"]}'
                for r in sorted(members, key=lambda x: int(x["row_index"]))
            )
            + "\n"
        )
        for sample, members in sorted(groups.items())
    }


def stratum_counts(rows: list[dict]) -> dict:
    out: dict[str, int] = {}
    for r in rows:
        k = r.get("selection_stratum", "backfill")
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


def community_counts(rows: list[dict]) -> dict:
    out: dict[str, int] = {}
    for r in rows:
        out[r["sample"]] = out.get(r["sample"], 0) + 1
    return dict(sorted(out.items()))


def scorer_function_digest(rows: list[dict]) -> str | None:
    """Digest produced by the gate's own hasher, not by this reimplementation.

    `score_coder_reliability.manifest_sha256` is the function that enforces the
    frozen sample before scoring agreement. If it returns something other than
    the frozen constant for the sampler's own output, the defect is in the record
    and not in how this script renders the manifest.
    """
    path = CODE / "score_coder_reliability.py"
    spec = importlib.util.spec_from_file_location("_scr", path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        keyed = {str(r["row_index"]): dict(r) for r in rows}
        for row in keyed.values():
            row.setdefault("source_row_index", str(row["row_index"]))
        return module.manifest_sha256(keyed)
    except Exception as exc:  # noqa: BLE001
        print(f"scorer-function check unavailable: {type(exc).__name__}: {exc}")
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--cached-payload",
        type=Path,
        help="Reuse a previously captured build_audit_sample.py JSON payload instead of hitting OSF.",
    )
    ap.add_argument("--out", type=Path, default=Path("manifest_digest_diagnosis.json"))
    args = ap.parse_args()

    if args.cached_payload:
        payload = json.loads(args.cached_payload.read_text(encoding="utf-8"))
    else:
        payload = regenerate_sampler_output()

    rows = payload.get("rows", [])
    canonical_text = exporter_manifest(rows)
    observed = digest(canonical_text)
    scorer_digest = scorer_function_digest(rows)

    matches = [vid for vid, body in serialisations(rows) if digest(body) == EXPECTED_MANIFEST_SHA256]
    observed_variants = {
        "utf8_lf": digest(canonical_text),
        "utf8_bom_lf": hashlib.sha256(b"\xef\xbb\xbf" + canonical_text.encode("utf-8")).hexdigest(),
        "utf8_crlf": digest(canonical_text.replace("\n", "\r\n")),
    }

    report = {
        "project": "ARIS4C016",
        "expected_frozen_manifest_sha256": EXPECTED_MANIFEST_SHA256,
        "observed_manifest_sha256": observed,
        "gate_function_manifest_sha256": scorer_digest,
        "observed_manifest_sha256_variants": observed_variants,
        "reproducible": observed == EXPECTED_MANIFEST_SHA256,
        "gate_function_agrees_with_observed": scorer_digest == observed,
        "n_rows": len(rows),
        "n_rows_expected": EXPECTED_N,
        "source_sha256_claimed_by_sampler": payload.get("source_sha256"),
        "target_policy": payload.get("target_policy"),
        "community_counts": community_counts(rows),
        "stratum_counts": stratum_counts(rows),
        "serialization_variants_tested": sum(1 for _ in serialisations(rows)),
        "serialization_variants_matching_frozen_digest": matches,
        "partial_digests_for_cross_check": partial_digests(rows),
        "per_sample_digests_for_cross_check": per_sample_digests(rows),
        "privacy_note": "Row indices, hashes and strata only; no lexical item or translation.",
    }
    args.out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
