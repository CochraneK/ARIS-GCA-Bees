#!/usr/bin/env python3
"""Fold the second-review adjudication into a CANDIDATE identity100 table.

The frozen protocol requires every first/second-review disagreement to be settled
by evidence adjudication before a person enters the confirmatory frame. This tool
applies exactly the adjudicated rows and nothing else, and it deliberately does
NOT overwrite ``data/derived/identity_decisions_100.csv``: the first review stays
immutable, and the merged table is a candidate until the pre-exposure frame
freeze is signed, because changing an included Author ID set invalidates the
downstream verified-work corpus and network frame.

Rows outside the adjudication file are copied verbatim, and the script fails if
any of them differs.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

FINAL_ALLOWED = {
    "VERIFIED_SINGLE",
    "VERIFIED_CLUSTER",
    "AMBIGUOUS_COLLISION",
    "NO_GRAPH_RECORD",
    "EXCLUDED_IDENTITY_ERROR",
}
VERIFIED = {"VERIFIED_SINGLE", "VERIFIED_CLUSTER"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_ids(value: str) -> list[str]:
    seen: list[str] = []
    for part in (value or "").replace(",", ";").split(";"):
        pid = part.strip()
        if pid and pid not in seen:
            seen.append(pid)
    return seen


def merge(rows: list[dict[str, str]], adjudications: list[dict[str, str]], *, date: str):
    """Return (merged_rows, per_case_change_records). Fails closed on bad input."""
    by_pid = {r["person_id"]: r for r in rows}
    if len(by_pid) != len(rows):
        raise SystemExit("identity table contains duplicate person_id")
    if len({a["person_id"] for a in adjudications}) != len(adjudications):
        raise SystemExit("adjudication file contains duplicate person_id")

    changes = []
    for adj in adjudications:
        pid = (adj.get("person_id") or "").strip()
        row = by_pid.get(pid)
        if row is None:
            raise SystemExit(f"adjudicated person_id absent from identity table: {pid}")
        name = (adj.get("canonical_name") or "").strip()
        if name and name != (row.get("canonical_name") or "").strip():
            raise SystemExit(f"{pid}: adjudication name {name!r} != table {row.get('canonical_name')!r}")
        status = (adj.get("adjudicated_status") or "").strip()
        if status not in FINAL_ALLOWED:
            raise SystemExit(f"{pid}: invalid adjudicated_status {status!r}")
        ids = split_ids(adj.get("adjudicated_ids") or "")
        if status in VERIFIED and not ids:
            raise SystemExit(f"{pid}: {status} requires at least one Author ID")
        if status == "VERIFIED_SINGLE" and len(ids) != 1:
            raise SystemExit(f"{pid}: VERIFIED_SINGLE must carry exactly one Author ID, got {len(ids)}")
        if status == "VERIFIED_CLUSTER" and len(ids) < 2:
            raise SystemExit(f"{pid}: VERIFIED_CLUSTER requires two or more Author IDs, got {len(ids)}")
        if status not in VERIFIED and ids:
            raise SystemExit(f"{pid}: {status} must carry an empty Author-ID set")
        if (adj.get("invented_ids_dropped") or "").strip():
            raise SystemExit(f"{pid}: adjudication dropped invented ids, re-run retrieval first")
        if (adj.get("deciding_evidence") or "").strip() == "":
            raise SystemExit(f"{pid}: adjudication has no deciding evidence recorded")

        before_status = (row.get("identity_status") or "").strip()
        before_ids = split_ids(row.get("verified_openalex_ids") or "")
        row["identity_status"] = status
        row["verified_openalex_ids"] = ";".join(ids)
        row["adjudication_status"] = "second-review-adjudicated"
        row["second_reviewer"] = (adj.get("adjudicator") or "").strip()
        row["review_date"] = date
        row["notes"] = (
            f"second-review adjudication ({date}): first={before_status}"
            f"[{';'.join(before_ids) or '-'}] -> {status}[{';'.join(ids) or '-'}]; "
            f"{(adj.get('deciding_evidence') or '').strip()}"
        )[:900]
        changes.append({
            "person_id": pid,
            "canonical_name": row.get("canonical_name", ""),
            "before_status": before_status,
            "after_status": status,
            "before_ids": before_ids,
            "after_ids": ids,
            "ids_added": sorted(set(ids) - set(before_ids)),
            "ids_removed": sorted(set(before_ids) - set(ids)),
            "retrieval_needed": (adj.get("retrieval_needed") or "").strip().lower() == "true",
        })
    return rows, changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--identity-table", type=Path, required=True,
                    help="Frozen first-review identity100 table (read only).")
    ap.add_argument("--adjudications", type=Path, required=True,
                    help="Completed second-review adjudication CSV.")
    ap.add_argument("--output", type=Path, required=True,
                    help="Candidate merged table. Must not be the input table.")
    ap.add_argument("--summary-json", type=Path, required=True)
    ap.add_argument("--review-date", default="2026-09-19")
    args = ap.parse_args()

    if args.output.resolve() == args.identity_table.resolve():
        raise SystemExit("refusing to overwrite the frozen identity table")

    original = read_csv(args.identity_table)
    rows = [dict(r) for r in original]
    merged, changes = merge(rows, read_csv(args.adjudications), date=args.review_date)

    touched = {c["person_id"] for c in changes}
    header = list(original[0])
    for col in ("identity_status", "verified_openalex_ids", "adjudication_status",
                "second_reviewer", "review_date", "notes"):
        if col not in header:
            raise SystemExit(f"identity table lacks required column {col!r}")
    for before, after in zip(original, merged):
        pid = before["person_id"]
        if pid in touched:
            continue
        if before != after:
            raise SystemExit(f"non-adjudicated row mutated: {pid}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=header, lineterminator="\n")
        w.writeheader()
        w.writerows(merged)

    def distribution(rs):
        return dict(sorted(Counter((r.get("identity_status") or "").strip() for r in rs).items()))

    summary = {
        "source_identity_table": args.identity_table.as_posix(),
        "candidate_output": args.output.as_posix(),
        "canonical_table_overwritten": False,
        "rows": len(merged),
        "adjudicated_rows_applied": len(changes),
        "status_distribution_before": distribution([r for r in original if r["person_id"] in touched]),
        "status_distribution_after": distribution([r for r in merged if r["person_id"] in touched]),
        "status_changes": sum(1 for c in changes if c["before_status"] != c["after_status"]),
        "id_set_changes": sum(1 for c in changes if c["before_ids"] != c["after_ids"]),
        "author_ids_added": sum(len(c["ids_added"]) for c in changes),
        "author_ids_removed": sum(len(c["ids_removed"]) for c in changes),
        "cases_still_flagged_for_retrieval": sorted(
            c["person_id"] for c in changes if c["retrieval_needed"]
        ),
        "changes": changes,
        "downstream_note": (
            "Changing an included Author-ID set invalidates the verified-work corpus and "
            "the network100 frame; this candidate table is not the confirmatory frame until "
            "PREEXPOSURE_FRAME_FREEZE.md is re-derived and signed."
        ),
    }
    args.summary_json.parent.mkdir(parents=True, exist_ok=True)
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "changes"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
