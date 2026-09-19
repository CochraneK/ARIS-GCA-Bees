#!/usr/bin/env python3
"""Validate and collect completed AI adjudication batch outputs.

The collector is fail-closed:
- every manifest batch must have exactly one completed output file;
- output assignments must exactly match the manifest checksum;
- row counts, adjudicator IDs and prompt versions must match;
- duplicate assignments are rejected;
- controlled-vocabulary fields are validated;
- collected outputs are separated by adjudicator.

Recommended output filename convention:
    <input_batch_stem>_output.csv
Example:
    AI_A_batch_001.csv -> AI_A_batch_001_output.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

ARTICLE_STATES = {
    "SEVERE_SUPPORTED",
    "SERIOUS_UNRESOLVED",
    "HONEST_MAJOR_ERROR",
    "MINOR_OR_IMMATERIAL",
    "NO_MATERIAL_PROBLEM_FOUND",
    "INDETERMINATE",
}
ARTICLE_MATERIALITY = {
    "MATERIAL",
    "POTENTIALLY_MATERIAL",
    "IMMATERIAL",
    "NOT_ASSESSABLE",
}
ARTICLE_MISCONDUCT = {
    "FORMAL_FINDING",
    "STRONG_DOCUMENTED_EVIDENCE",
    "SUSPECTED_NOT_ESTABLISHED",
    "NO_EVIDENCE_OF_MISCONDUCT",
    "NOT_ASSESSABLE",
}
CITATION_SEMANTIC = {
    "BACKGROUND_MENTION",
    "METHOD_REUSE",
    "RESULT_DEPENDENCE",
    "EVIDENCE_SYNTHESIS_INCLUDE",
    "CRITIQUE_OR_CORRECTION",
    "CITATION_ONLY_OR_PERIPHERAL",
    "INDETERMINATE",
}
YES_NO_UNKNOWN = {"YES", "NO", "UNKNOWN"}
CITATION_ACCESS = {"FULLTEXT", "ABSTRACT_ONLY", "NO_CONTEXT"}
CONFIDENCE = {"HIGH", "MEDIUM", "LOW"}


def norm(value: str | None) -> str:
    return (value or "").strip().upper()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                fields.append(key)
                seen.add(key)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def checksum_rows(
    rows: list[dict[str, str]],
    id_fields: tuple[str, str],
) -> str:
    ordered = sorted(rows, key=lambda r: (r.get("assignment_id") or ""))
    h = hashlib.sha256()
    for row in ordered:
        payload = "|".join(str(row.get(field, "")) for field in id_fields)
        h.update(payload.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def derived_output_filename(input_filename: str, suffix: str) -> str:
    p = Path(input_filename)
    return p.stem + suffix + p.suffix


def require_nonempty(row: dict[str, str], fields: list[str], label: str) -> None:
    for field in fields:
        if not (row.get(field) or "").strip():
            raise ValueError(f"{label}: missing required field {field}")


def validate_article_row(row: dict[str, str], reviewer: str) -> None:
    require_nonempty(
        row,
        [
            "assignment_id",
            "paper_id",
            "adjudicator_id",
            "model_name",
            "model_version_or_snapshot",
            "prompt_version",
            "run_id",
            "scientific_state",
            "materiality",
            "misconduct_evidence",
            "review_confidence",
            "brief_evidence_rationale",
        ],
        row.get("assignment_id") or "<article-row>",
    )
    if (row.get("adjudicator_id") or "").strip() != reviewer:
        raise ValueError(
            f"{row.get('assignment_id')}: adjudicator_id does not match manifest"
        )
    if (row.get("prompt_version") or "").strip() != "AI-ADJ-V1":
        raise ValueError(
            f"{row.get('assignment_id')}: prompt_version must be AI-ADJ-V1"
        )
    if norm(row.get("scientific_state")) not in ARTICLE_STATES:
        raise ValueError(f"{row.get('assignment_id')}: invalid scientific_state")
    if norm(row.get("materiality")) not in ARTICLE_MATERIALITY:
        raise ValueError(f"{row.get('assignment_id')}: invalid materiality")
    if norm(row.get("misconduct_evidence")) not in ARTICLE_MISCONDUCT:
        raise ValueError(f"{row.get('assignment_id')}: invalid misconduct_evidence")
    if norm(row.get("review_confidence")) not in CONFIDENCE:
        raise ValueError(f"{row.get('assignment_id')}: invalid review_confidence")
    if norm(row.get("scientific_state")) == "INDETERMINATE":
        if not (row.get("abstain_reason") or "").strip():
            raise ValueError(
                f"{row.get('assignment_id')}: INDETERMINATE requires abstain_reason"
            )


def validate_citation_row(row: dict[str, str], adjudicator: str) -> None:
    require_nonempty(
        row,
        [
            "assignment_id",
            "edge_id",
            "adjudicator_id",
            "model_name",
            "model_version_or_snapshot",
            "prompt_version",
            "run_id",
            "semantic_class",
            "component_implicated",
            "material_to_downstream_claim",
            "source_retraction_known_in_text",
            "context_access",
            "review_confidence",
            "brief_evidence_rationale",
        ],
        row.get("assignment_id") or "<citation-row>",
    )
    if (row.get("adjudicator_id") or "").strip() != adjudicator:
        raise ValueError(
            f"{row.get('assignment_id')}: adjudicator_id does not match manifest"
        )
    if (row.get("prompt_version") or "").strip() != "CIT-EDGE-V1":
        raise ValueError(
            f"{row.get('assignment_id')}: prompt_version must be CIT-EDGE-V1"
        )
    if norm(row.get("semantic_class")) not in CITATION_SEMANTIC:
        raise ValueError(f"{row.get('assignment_id')}: invalid semantic_class")
    for field in (
        "component_implicated",
        "material_to_downstream_claim",
        "source_retraction_known_in_text",
    ):
        if norm(row.get(field)) not in YES_NO_UNKNOWN:
            raise ValueError(f"{row.get('assignment_id')}: invalid {field}")
    if norm(row.get("context_access")) not in CITATION_ACCESS:
        raise ValueError(f"{row.get('assignment_id')}: invalid context_access")
    if norm(row.get("review_confidence")) not in CONFIDENCE:
        raise ValueError(f"{row.get('assignment_id')}: invalid review_confidence")
    if norm(row.get("semantic_class")) == "INDETERMINATE":
        if not (row.get("abstain_reason") or "").strip():
            raise ValueError(
                f"{row.get('assignment_id')}: INDETERMINATE requires abstain_reason"
            )


def collect(
    manifest: dict[str, Any],
    output_dir: Path,
    *,
    mode: str,
    output_suffix: str = "_output",
) -> tuple[dict[str, list[dict[str, str]]], dict[str, Any]]:
    if mode not in {"article", "citation"}:
        raise ValueError("mode must be article or citation")

    if mode == "article":
        expected_class = "AI_ADJUDICATION_BATCH_MANIFEST_NO_LABELS"
        person_key = "reviewer_id"
        people = manifest.get("reviewers") or {}
        id_fields = ("assignment_id", "paper_id")
        validator = validate_article_row
    else:
        expected_class = "CITATION_EDGE_AI_BATCH_MANIFEST_NO_LABELS"
        person_key = "adjudicator_id"
        people = manifest.get("adjudicators") or {}
        id_fields = ("assignment_id", "edge_id")
        validator = validate_citation_row

    if manifest.get("classification") != expected_class:
        raise ValueError(
            f"Manifest classification mismatch for mode={mode}: "
            f"{manifest.get('classification')!r}"
        )

    batches = manifest.get("batches")
    if not isinstance(batches, list) or not batches:
        raise ValueError("manifest has no batches")

    collected: dict[str, list[dict[str, str]]] = defaultdict(list)
    batch_summaries = []
    global_assignments: set[str] = set()

    for batch in batches:
        person = str(batch.get(person_key) or "").strip()
        if not person:
            raise ValueError(f"batch missing {person_key}")
        input_filename = str(batch.get("filename") or "").strip()
        output_filename = derived_output_filename(input_filename, output_suffix)
        path = output_dir / output_filename
        if not path.exists():
            raise FileNotFoundError(
                f"Missing completed batch output: {output_filename}"
            )

        rows = read_csv(path)
        expected_n = int(batch["assignments"])
        if len(rows) != expected_n:
            raise ValueError(
                f"{output_filename}: expected {expected_n} rows, got {len(rows)}"
            )

        local_ids: set[str] = set()
        for row in rows:
            aid = (row.get("assignment_id") or "").strip()
            if not aid:
                raise ValueError(f"{output_filename}: missing assignment_id")
            if aid in local_ids:
                raise ValueError(f"{output_filename}: duplicate assignment_id {aid}")
            if aid in global_assignments:
                raise ValueError(f"assignment_id appears in multiple batches: {aid}")
            local_ids.add(aid)
            global_assignments.add(aid)
            validator(row, person)

        observed_checksum = checksum_rows(rows, id_fields)
        expected_checksum = str(batch.get("assignment_checksum_sha256") or "")
        if observed_checksum != expected_checksum:
            raise ValueError(
                f"{output_filename}: assignment checksum mismatch; "
                f"expected {expected_checksum}, observed {observed_checksum}"
            )

        collected[person].extend(
            sorted(rows, key=lambda r: r["assignment_id"])
        )
        batch_summaries.append(
            {
                "person_id": person,
                "batch_number": int(batch["batch_number"]),
                "output_filename": output_filename,
                "assignments": len(rows),
                "assignment_checksum_sha256": observed_checksum,
                "status": "VALID",
            }
        )

    expected_total = int(manifest["assignments_total"])
    if len(global_assignments) != expected_total:
        raise ValueError(
            f"Expected {expected_total} unique assignments, got "
            f"{len(global_assignments)}"
        )

    for person, expected in people.items():
        observed = len(collected.get(person, []))
        if observed != int(expected):
            raise ValueError(
                f"{person}: expected {expected} assignments, got {observed}"
            )

    summary = {
        "classification": (
            "AI_BATCH_OUTPUT_COLLECTION_VALIDATED_NOT_GOLD_STANDARD_LABELS"
            if mode == "article"
            else "CITATION_AI_BATCH_OUTPUT_COLLECTION_VALIDATED_NOT_GOLD_STANDARD_LABELS"
        ),
        "mode": mode,
        "manifest_classification": manifest["classification"],
        "expected_batches": len(batches),
        "validated_batches": len(batch_summaries),
        "expected_assignments_total": expected_total,
        "validated_unique_assignments": len(global_assignments),
        "assignments_by_person": {
            person: len(rows) for person, rows in sorted(collected.items())
        },
        "batch_summaries": batch_summaries,
        "warnings": [
            "Successful collection verifies batch integrity and schema, not label correctness.",
            "AI outputs remain fallible measurements and still require arbitration/calibration.",
        ],
    }
    return dict(collected), summary


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("manifest_json", type=Path)
    p.add_argument("output_dir", type=Path)
    p.add_argument("collected_dir", type=Path)
    p.add_argument("summary_json", type=Path)
    p.add_argument("--mode", required=True, choices=["article", "citation"])
    p.add_argument("--output-suffix", default="_output")
    args = p.parse_args()

    manifest = json.loads(args.manifest_json.read_text(encoding="utf-8"))
    collected, summary = collect(
        manifest,
        args.output_dir,
        mode=args.mode,
        output_suffix=args.output_suffix,
    )

    args.collected_dir.mkdir(parents=True, exist_ok=True)
    for person, rows in collected.items():
        write_csv(args.collected_dir / f"{person}_collected.csv", rows)

    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
