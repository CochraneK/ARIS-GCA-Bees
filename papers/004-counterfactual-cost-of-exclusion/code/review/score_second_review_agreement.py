"""ARIS4C004 second-review agreement scorer .

Run only AFTER the 40 independent judgments are frozen. Implements the
Precision reporting section of IDENTITY_SECOND_REVIEW_PROTOCOL.md.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
from collections import Counter
from pathlib import Path

_PAPER_DIR = os.environ.get("ARIS4C_PAPER_DIR")
PAPER = Path(_PAPER_DIR) if _PAPER_DIR else Path(__file__).resolve().parents[2]
VERIFIED = ("VERIFIED_SINGLE", "VERIFIED_CLUSTER")


def ids(s: str) -> frozenset:
    return frozenset(x.strip() for x in (s or "").split(";") if x.strip())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--first", type=Path, default=PAPER / "data" / "derived" / "identity_decisions_100.csv")
    ap.add_argument("--second", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--disagreements", type=Path, required=True)
    a = ap.parse_args()

    first = {r["person_id"]: r for r in csv.DictReader(a.first.open(encoding="utf-8-sig", newline=""))}
    second = list(csv.DictReader(a.second.open(encoding="utf-8-sig", newline="")))
    assert len(second) == 40, f"expected 40 second-review rows, got {len(second)}"

    rows = []
    for s in second:
        f = first[s["person_id"]]
        fs, ss = f["identity_status"].strip(), s["second_review_status"].strip()
        fi, si = ids(f["verified_openalex_ids"]), ids(s["second_review_openalex_ids"])
        state_match = fs == ss
        id_match = (fi == si) if (state_match and fs in VERIFIED) else None
        rows.append({
            "person_id": s["person_id"],
            "canonical_name": s["canonical_name"],
            "first_status": fs,
            "second_status": ss,
            "first_ids": ";".join(sorted(fi)),
            "second_ids": ";".join(sorted(si)),
            "state_match": state_match,
            "id_set_match": id_match,
            "extra_ids_second": ";".join(sorted(si - fi)),
            "missing_ids_second": ";".join(sorted(fi - si)),
            "notes": s.get("notes", ""),
        })

    n = len(rows)
    sm = [r for r in rows if r["state_match"]]
    verified_pairs = [r for r in rows if r["id_set_match"] is not None]
    by_first = Counter(r["first_status"] for r in rows)
    by_second = Counter(r["second_status"] for r in rows)

    def split(pred):
        sub = [r for r in rows if pred(r)]
        return {
            "n": len(sub),
            "state_agreement": round(sum(r["state_match"] for r in sub) / len(sub), 4) if sub else None,
            "id_set_agreement": (
                round(sum(bool(r["id_set_match"]) for r in sub if r["id_set_match"] is not None)
                      / len([r for r in sub if r["id_set_match"] is not None]), 4)
                if any(r["id_set_match"] is not None for r in sub) else None
            ),
        }

    summary = {
        "classification": "IDENTITY_SECOND_REVIEW_AGREEMENT",
        "n_second_reviewed": n,
        "exact_state_agreement": round(len(sm) / n, 4),
        "exact_author_id_set_agreement_where_state_matches_and_verified": (
            round(sum(bool(r["id_set_match"]) for r in verified_pairs) / len(verified_pairs), 4)
            if verified_pairs else None
        ),
        "first_review_state_counts": dict(by_first),
        "second_review_state_counts": dict(by_second),
        "false_positive_identity_mapping_count": sum(
            1 for r in rows
            if r["first_status"] in VERIFIED and r["second_status"] not in VERIFIED
        ),
        "missed_fragment_count": sum(len(ids(r["extra_ids_second"])) for r in rows),
        "first_only_fragment_count": sum(len(ids(r["missing_ids_second"])) for r in rows),
        "collision_or_error_reversals": sum(
            1 for r in rows
            if r["first_status"] in VERIFIED
            and r["second_status"] in ("AMBIGUOUS_COLLISION", "EXCLUDED_IDENTITY_ERROR")
        ),
        "agreement_by_first_state": {
            "VERIFIED_SINGLE": split(lambda r: r["first_status"] == "VERIFIED_SINGLE"),
            "VERIFIED_CLUSTER": split(lambda r: r["first_status"] == "VERIFIED_CLUSTER"),
            "AMBIGUOUS_COLLISION": split(lambda r: r["first_status"] == "AMBIGUOUS_COLLISION"),
            "NO_GRAPH_RECORD": split(lambda r: r["first_status"] == "NO_GRAPH_RECORD"),
            "EXCLUDED_IDENTITY_ERROR": split(lambda r: r["first_status"] == "EXCLUDED_IDENTITY_ERROR"),
        },
        "disagreement_count": n - len(sm),
        "note": (
            "Second review produced on a separate AI execution surface from scripted public-evidence "
            "retrieval; it is an independent machine review, not a second human identity curator."
        ),
    }

    a.output.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    with a.disagreements.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows([r for r in rows if not r["state_match"] or r["id_set_match"] is False])
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
