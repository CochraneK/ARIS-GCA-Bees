"""Build leakage-separated ARIS4C011 Benchmark-v0 manifests.

Input is an adjudication table whose *target* work has already been resolved.
The builder intentionally separates full provenance from the content-only
Track-A manifest. It never converts a retraction into a misconduct label.

Minimum input columns:
    target_doi, target_title_safe, target_year, target_journal,
    notice_type, notice_date, raw_reason, source_url

Optional provenance columns can include assertion/event IDs, notice DOI,
Retraction Watch record ID, raw current title, and cluster IDs.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Dict, Iterable, List, Set


SCHEMA_VERSION = "0.2.0"

REQUIRED = {
    "target_doi", "target_title_safe", "target_year", "target_journal",
    "notice_type", "notice_date", "raw_reason", "source_url",
}

# These fields are outcome/post-publication provenance and are categorically
# excluded from Track A. A deny-list is still recorded for audit, while
# Track-A rows are constructed from an explicit allow-list below.
LABEL_PROVENANCE_FIELDS = {
    "raw_reason",
    "notice_type",
    "notice_date",
    "source_url",
    "candidate_issue_codes",
    "ground_truth_tier",
    "event_key",
    "assertion_key",
    "notice_doi",
    "crossref_source_work_doi",
    "relation_type",
    "relation_label",
    "assertion_source",
    "update_date",
    "retraction_watch_record_id",
    "target_title_raw_current",
    "title_status_marker",
    "current_metadata_contains_update_relations",
}

TRACK_A_MANIFEST_ALLOWLIST = [
    "paper_id",
    "target_title_safe",
    "article_type",
    "fulltext_ref",
    "track_a_title_requires_historical_validation",
    "track_a_document_safe",
    "split",
]

# Only these fields may be passed directly as tabular/model features by the
# benchmark loader. IDs, paths, split labels, venue/year and cluster IDs are
# never model features in the primary content-only task.
TRACK_A_FEATURE_ALLOWLIST = [
    "target_title_safe",
]

ISSUE_RULES = {
    "image_integrity": [
        r"image", r"figure", r"western blot", r"gel",
        r"duplica(?:te|tion).*panel", r"manipulat.*(?:image|figure)",
    ],
    "plagiarism_text_duplication": [
        r"plagiarism", r"text overlap", r"duplicate publication", r"redundan(?:t|cy)",
    ],
    "statistical_reporting": [
        r"statistic", r"analysis error", r"calculation error",
        r"incorrect p[- ]?value", r"data analysis",
    ],
    "data_fabrication_falsification": [
        r"fabricat", r"falsif", r"made[- ]?up data",
    ],
    "paper_mill": [
        r"paper mill", r"systematic manipulation",
    ],
    "authorship_peer_review": [
        r"authorship", r"gift author", r"peer review", r"reviewer",
        r"editorial process.*compromis", r"peer review process.*manipulat",
    ],
    "citation_reference": [
        r"citation", r"reference", r"bibliograph",
    ],
    "registration_ethics_provenance": [
        r"ethic", r"consent", r"registration", r"protocol", r"approval",
    ],
}


def normalize_doi(value: str) -> str:
    x = (value or "").strip().lower()
    x = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", x)
    x = re.sub(r"^doi:\s*", "", x)
    return x.strip()


def paper_id_for_doi(doi: str) -> str:
    raw = ("paper:" + normalize_doi(doi)).encode("utf-8")
    return "p_" + hashlib.sha256(raw).hexdigest()[:16]


def issue_codes(reason: str) -> List[str]:
    """Rule-based candidates for HUMAN adjudication; never final truth labels."""
    text = (reason or "").lower()
    found: Set[str] = set()
    for code, patterns in ISSUE_RULES.items():
        if any(re.search(p, text) for p in patterns):
            found.add(code)
    return sorted(found) or ["other_unclear"]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_rows(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    fields = set(rows[0].keys() if rows else [])
    missing = REQUIRED - fields
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return rows


def enrich(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    out = []
    seen = set()
    for row in rows:
        r = dict(row)
        r["target_doi"] = normalize_doi(r.get("target_doi", ""))
        key = (
            r["target_doi"],
            (r.get("notice_type") or "").strip().lower(),
            (r.get("notice_date") or "").strip(),
        )
        if key in seen:
            continue
        seen.add(key)

        r["paper_id"] = paper_id_for_doi(r["target_doi"])
        r["candidate_issue_codes"] = ";".join(issue_codes(r.get("raw_reason", "")))
        r.setdefault("ground_truth_tier", "")
        r.setdefault("known_cluster_id", "")
        r.setdefault("text_cluster_id", "")
        r.setdefault("image_cluster_id", "")
        r.setdefault("article_type", "")
        r.setdefault("fulltext_ref", "")
        r.setdefault("split", "")
        r.setdefault("track_a_title_requires_historical_validation", "0")
        r.setdefault("track_a_document_safe", "0")
        r["track_a_eligible"] = (
            "1"
            if r["target_doi"]
            and r.get("track_a_title_requires_historical_validation") == "0"
            and r.get("track_a_document_safe") == "1"
            else "0"
        )
        r["track_b_eligible"] = "1"
        out.append(r)
    return out


def write_csv(path: Path, rows: List[Dict[str, str]], fields: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def track_a_rows(rows: List[Dict[str, str]]) -> tuple[List[Dict[str, str]], List[str]]:
    fields = [f for f in TRACK_A_MANIFEST_ALLOWLIST if any(f in r for r in rows)]
    projected = [{f: r.get(f, "") for f in fields} for r in rows]
    return projected, fields


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print("Usage: python build_benchmark_v0.py adjudicated.csv out_dir", file=sys.stderr)
        return 2

    src = Path(argv[1])
    out_dir = Path(argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = enrich(read_rows(src))
    if not rows:
        raise ValueError("Input contained no rows.")

    all_fields = list(dict.fromkeys(k for r in rows for k in r))
    full_path = out_dir / "benchmark_full.csv"
    write_csv(full_path, rows, all_fields)

    projected, track_a_fields = track_a_rows(rows)
    track_a = out_dir / "track_a_manifest.csv"
    write_csv(track_a, projected, track_a_fields)

    track_b = out_dir / "track_b_manifest.csv"
    write_csv(track_b, rows, all_fields)

    meta = {
        "schema_version": SCHEMA_VERSION,
        "source_file": src.name,
        "source_sha256": sha256_file(src),
        "rows_after_deduplication": len(rows),
        "full_sha256": sha256_file(full_path),
        "track_a_sha256": sha256_file(track_a),
        "track_b_sha256": sha256_file(track_b),
        "track_a_manifest_allowlist": TRACK_A_MANIFEST_ALLOWLIST,
        "track_a_feature_allowlist": TRACK_A_FEATURE_ALLOWLIST,
        "track_a_label_provenance_fields": sorted(LABEL_PROVENANCE_FIELDS),
        "warning": (
            "candidate_issue_codes are weak rule-based triage labels and require "
            "human adjudication. Track A also requires a clean pre-outcome document; "
            "sanitizing a title alone is insufficient."
        ),
    }
    (out_dir / "benchmark_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
