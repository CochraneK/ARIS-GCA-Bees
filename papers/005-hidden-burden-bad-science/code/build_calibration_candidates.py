#!/usr/bin/env python3
"""Build *review candidates* for AI calibration from classified Retraction Watch data.

Important boundary:
- This script does NOT create calibration truth labels.
- It creates queues for later notice/institutional-evidence review.
- Row-level candidate output is intended for private/ephemeral review only.
- Public repository outputs should contain aggregate counts only.

Candidate queues:
P_HIGH_REVIEW
    Narrow fabrication/falsification signal plus an official/misconduct finding
    context reason. Still requires source-document confirmation.
P_REVIEW
    Narrow fabrication/falsification signal without enough evidence here to
    assign reference truth.
N_PROCESS_REVIEW
    Narrow process-only reason family with no scientific unreliability signal.
    Still requires explicit evidence that the scientific claim is unaffected.
U_REVIEW
    Everything else; not suitable for primary calibration without more evidence.

The design is intentionally conservative because Retraction Watch reasons are
screening metadata, not reference-standard truth.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from classify_retractions import (
    CONTEXT_ONLY,
    E1S_NARROW,
    E3_ERROR,
    MANUAL_SCIENTIFIC_REVIEW,
    normalize_reason,
    split_reasons,
    vocab,
)


NEGATIVE_PROCESS_ONLY = vocab(
    "Plagiarism of/in Article",
    "Plagiarism of Text",
    "Euphemisms for Plagiarism",
    "Concerns/Issues about Authorship/Affiliation",
    "False/Forged Authorship",
    "False/Forged Affiliation",
    "Compromised Peer Review",
    "Concerns/Issues about Peer Review",
    "Concerns/Issues with Peer Review",
)

POSITIVE_FINDING_CONTEXT = vocab(
    "Misconduct - Official Investigation(s) and/or Finding(s)",
    "Misconduct by Author",
    "Investigation by ORI",
    "Investigation by Company/Institution",
)

FLAG_FIELDS = (
    "e1s_narrow_auto",
    "e1m_strong_auto",
    "e1p_strong_auto",
    "paper_mill_signal",
    "e3_error_signal",
    "manual_scientific_review",
    "manual_process_review",
    "context_only_reasons",
)


def norm_doi(raw: str | None) -> str:
    value = (raw or "").strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if value.startswith(prefix):
            value = value[len(prefix):]
    if value in {"", "none", "nan", "unavailable", "0"}:
        return ""
    return value.strip()


def int_flag(value: str | None) -> int:
    try:
        return 1 if int(value or 0) else 0
    except ValueError:
        return 0


def parse_year(raw: str | None) -> int | None:
    text = (raw or "").strip()
    match = re.search(r"(?<!\d)(1[6-9]\d{2}|20\d{2}|2100)(?!\d)", text)
    return int(match.group(1)) if match else None


def candidate_queue(
    reasons: set[str],
    natures: set[str],
    flags: dict[str, int],
) -> tuple[str, str]:
    e1s = bool(flags.get("e1s_narrow_auto")) or bool(reasons & E1S_NARROW)
    e1m = bool(flags.get("e1m_strong_auto"))
    e1p = bool(flags.get("e1p_strong_auto"))
    e3 = bool(flags.get("e3_error_signal")) or bool(reasons & E3_ERROR)
    manual_scientific = bool(flags.get("manual_scientific_review")) or bool(
        reasons & MANUAL_SCIENTIFIC_REVIEW
    )
    paper_mill = bool(flags.get("paper_mill_signal"))

    if e1s:
        if reasons & POSITIVE_FINDING_CONTEXT:
            return (
                "P_HIGH_REVIEW",
                "narrow fabrication/falsification signal plus official/misconduct context; verify primary evidence",
            )
        return (
            "P_REVIEW",
            "narrow fabrication/falsification signal; verify notice/institutional evidence and materiality",
        )

    allowed_negative = NEGATIVE_PROCESS_ONLY | CONTEXT_ONLY
    has_process = bool(reasons & NEGATIVE_PROCESS_ONLY)
    process_only = (
        bool(reasons)
        and has_process
        and reasons.issubset(allowed_negative)
        and not e3
        and not manual_scientific
        and not paper_mill
    )
    if process_only:
        return (
            "N_PROCESS_REVIEW",
            "process-only screening reasons with no scientific unreliability flag; must verify claim unaffected",
        )

    honest_error_candidate = (
        e3
        and not e1s
        and not e1m
        and not e1p
        and not paper_mill
        and not manual_scientific
    )
    if honest_error_candidate:
        return (
            "N_ERROR_REVIEW",
            "error/reproducibility screening signal without strong integrity flags; must verify honest-error reference evidence",
        )

    return (
        "U_REVIEW",
        "insufficient or mixed screening evidence for calibration truth",
    )


def stable_hash(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def collapse_rows(rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    papers: dict[str, dict[str, Any]] = {}
    no_doi_rows = 0

    for row in rows:
        doi = norm_doi(row.get("OriginalPaperDOI"))
        if not doi:
            no_doi_rows += 1
            continue

        rec = papers.setdefault(
            doi,
            {
                "doi": doi,
                "titles": set(),
                "journals": set(),
                "publishers": set(),
                "years": set(),
                "natures": set(),
                "reasons": set(),
                "record_ids": set(),
                "flags": {field: 0 for field in FLAG_FIELDS},
            },
        )

        for field, key in (
            ("Title", "titles"),
            ("Journal", "journals"),
            ("Publisher", "publishers"),
            ("RetractionNature", "natures"),
            ("Record ID", "record_ids"),
        ):
            value = (row.get(field) or "").strip()
            if value:
                rec[key].add(value)

        year = parse_year(row.get("OriginalPaperDate"))
        if year is not None:
            rec["years"].add(year)

        for reason in split_reasons(row.get("Reason")):
            rec["reasons"].add(normalize_reason(reason))

        for field in FLAG_FIELDS:
            rec["flags"][field] = max(
                rec["flags"][field],
                int_flag(row.get(field)),
            )

    output: list[dict[str, Any]] = []
    queue_counts: Counter[str] = Counter()
    basis_counts: Counter[str] = Counter()

    priority = {
        "P_HIGH_REVIEW": 1,
        "P_REVIEW": 2,
        "N_PROCESS_REVIEW": 3,
        "N_ERROR_REVIEW": 4,
        "U_REVIEW": 5,
    }

    for doi, rec in papers.items():
        queue, basis = candidate_queue(
            rec["reasons"],
            rec["natures"],
            rec["flags"],
        )
        queue_counts[queue] += 1
        basis_counts[basis] += 1

        title = sorted(rec["titles"])[0] if rec["titles"] else ""
        journal = sorted(rec["journals"])[0] if rec["journals"] else ""
        publisher = sorted(rec["publishers"])[0] if rec["publishers"] else ""
        year = min(rec["years"]) if rec["years"] else ""

        cluster_basis = "|".join(
            [
                normalize_reason(publisher),
                normalize_reason(journal),
                queue,
                ";".join(sorted(rec["reasons"])),
            ]
        )

        output.append(
            {
                "candidate_id": "CALC_" + stable_hash(doi),
                "doi": doi,
                "title": title,
                "publication_year": year,
                "journal": journal,
                "publisher": publisher,
                "retraction_natures": "; ".join(sorted(rec["natures"])),
                "reasons": "; ".join(sorted(rec["reasons"])),
                "event_record_count": len(rec["record_ids"]),
                "candidate_queue": queue,
                "candidate_priority": priority[queue],
                "candidate_basis": basis,
                "provisional_cluster_id": "CL_" + stable_hash(cluster_basis, 12),
                "reference_binary_state": "",
                "reference_scientific_state": "",
                "anchor_quality": "",
                "requires_primary_evidence_review": 1,
                "public_row_level_release_allowed": 0,
            }
        )

    output.sort(
        key=lambda r: (
            int(r["candidate_priority"]),
            str(r["provisional_cluster_id"]),
            str(r["candidate_id"]),
        )
    )

    summary = {
        "classification": "CALIBRATION_CANDIDATE_QUEUE_NOT_REFERENCE_TRUTH",
        "unique_resolvable_dois": len(papers),
        "event_rows_without_resolvable_doi": no_doi_rows,
        "candidate_queue_counts": dict(queue_counts),
        "reference_truth_labels_assigned": 0,
        "public_row_level_release_allowed": False,
        "candidate_rules": {
            "P_HIGH_REVIEW": (
                "narrow fabrication/falsification screening signal plus official/misconduct context"
            ),
            "P_REVIEW": "narrow fabrication/falsification screening signal",
            "N_PROCESS_REVIEW": (
                "narrow process-only reason family with no scientific unreliability signal"
            ),
            "N_ERROR_REVIEW": (
                "E3 error/reproducibility signal without strong integrity flags; requires confirmation that the error is non-severe/non-misconduct"
            ),
            "U_REVIEW": "mixed/ambiguous/insufficient screening evidence",
        },
        "warnings": [
            "Retraction Watch reasons are screening metadata, not calibration truth.",
            "P candidates require notice/institutional primary-evidence confirmation and materiality review.",
            "N_PROCESS_REVIEW requires explicit evidence that the scientific claim is unaffected.",
            "N_ERROR_REVIEW is not automatically honest error; it requires primary evidence excluding severe integrity failure.",
            "Absence of a scientific flag is not a negative reference standard.",
            "Provisional cluster IDs are only de-duplication/review aids and do not prove statistical independence.",
            "Do not commit or publicly release the row-level candidate queue from a public repository.",
        ],
    }
    return output, summary


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("classified_rw_csv", type=Path)
    p.add_argument("private_candidate_csv", type=Path)
    p.add_argument("public_summary_json", type=Path)
    args = p.parse_args()

    candidates, summary = collapse_rows(read_csv(args.classified_rw_csv))
    write_csv(args.private_candidate_csv, candidates)
    args.public_summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.public_summary_json.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
