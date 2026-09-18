"""Build an ARIS4C011 Benchmark-v0 manifest from a normalized notice table.

This utility is intentionally conservative. It does not download private data,
does not label all retractions as misconduct, and never exposes label-defining
notice text to Track-A feature exports.

Expected input CSV columns (minimum):
    doi, title, year, journal, notice_type, notice_date, raw_reason, source_url

Optional:
    article_type, field, fulltext_available, ground_truth_tier,
    known_cluster_id, text_cluster_id, image_cluster_id

Usage:
    python build_benchmark_v0.py notices.csv out_dir

Outputs:
    benchmark_full.csv      provenance/label table for adjudication
    track_a_manifest.csv    content-only safe manifest (reason text removed)
    track_b_manifest.csv    open-world manifest
    benchmark_meta.json     hashes and schema version

This is infrastructure, not a classifier.
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Dict, Iterable, List, Set


SCHEMA_VERSION = "0.1.0"

ISSUE_RULES = {
    "image_integrity": [
        r"image", r"figure", r"western blot", r"gel", r"duplica(?:te|tion).*panel",
        r"manipulat.*(?:image|figure)",
    ],
    "plagiarism_text_duplication": [
        r"plagiarism", r"text overlap", r"duplicate publication", r"redundan(?:t|cy)",
    ],
    "statistical_reporting": [
        r"statistic", r"analysis error", r"calculation error", r"incorrect p[- ]?value",
        r"data analysis",
    ],
    "data_fabrication_falsification": [
        r"fabricat", r"falsif", r"made[- ]?up data",
    ],
    "paper_mill": [
        r"paper mill", r"systematic manipulation", r"compromised peer review",
    ],
    "citation_reference": [
        r"citation", r"reference", r"bibliograph",
    ],
    "authorship_peer_review": [
        r"authorship", r"peer review", r"reviewer",
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


def issue_codes(reason: str) -> List[str]:
    """Rule-based candidates for HUMAN adjudication; not final truth labels."""
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
    required = {
        "doi", "title", "year", "journal",
        "notice_type", "notice_date", "raw_reason", "source_url",
    }
    missing = required - set(rows[0].keys() if rows else [])
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return rows


def enrich(rows: Iterable[Dict[str, str]]) -> List[Dict[str, str]]:
    out = []
    seen = set()
    for row in rows:
        r = dict(row)
        r["doi"] = normalize_doi(r.get("doi", ""))
        key = (
            r["doi"],
            (r.get("notice_type") or "").strip().lower(),
            (r.get("notice_date") or "").strip(),
        )
        if key in seen:
            continue
        seen.add(key)

        # Candidate coding must be reviewed before GT-A/B/C confirmatory use.
        r["candidate_issue_codes"] = ";".join(issue_codes(r.get("raw_reason", "")))
        r.setdefault("ground_truth_tier", "")
        r.setdefault("known_cluster_id", "")
        r.setdefault("text_cluster_id", "")
        r.setdefault("image_cluster_id", "")
        r["track_a_eligible"] = "1" if r["doi"] else "0"
        r["track_b_eligible"] = "1"
        out.append(r)
    return out


def write_csv(path: Path, rows: List[Dict[str, str]], fields: List[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print("Usage: python build_benchmark_v0.py notices.csv out_dir", file=sys.stderr)
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

    # Track A MUST remove outcome-defining/post-publication text/status fields.
    forbidden_a = {
        "raw_reason", "notice_type", "notice_date", "source_url",
        "candidate_issue_codes", "ground_truth_tier",
    }
    track_a_fields = [f for f in all_fields if f not in forbidden_a]
    track_a = out_dir / "track_a_manifest.csv"
    write_csv(track_a, rows, track_a_fields)

    # Track B may use public post-publication information.
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
        "track_a_forbidden_fields": sorted(forbidden_a),
        "warning": (
            "candidate_issue_codes are weak rule-based triage labels and require "
            "human adjudication before confirmatory use."
        ),
    }
    (out_dir / "benchmark_meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
