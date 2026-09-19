#!/usr/bin/env python3
"""Audit the ARIS4C004 AI adjudication of the 23 identity disagreements.

The frozen protocol makes adjudication an evidence argument, not a tie-break, so
this checks structural properties the protocol cares about before anything is
consumed downstream:

- every included Author ID must be grounded in the retrieved packet;
- how often the adjudication is strictly BROADER than both reviews (the
  over-merge direction that inflates a person's output and dependence edges);
- how often it is strictly NARROWER (the direction the protocol prefers);
- whether unresolved cases were flagged for additional retrieval;
- status/ID-count consistency after normalization.

Reads only the local dossier and checkpoint. Emits aggregate counts plus a
per-case table; no exposure or mental-health field is touched.
"""
from __future__ import annotations

import csv
import json
import os
from pathlib import Path

CODE_DIR = Path(__file__).resolve().parent
HERE = Path(os.environ.get("ARIS4C004_REVIEW_SCRATCH") or (CODE_DIR / "_second_review_scratch"))
VERIFIED = {"VERIFIED_SINGLE", "VERIFIED_CLUSTER"}


def ids(s: str) -> set[str]:
    return {x for x in (s or "").split(";") if x}


def main() -> None:
    dossier = {r["person_id"]: r for r in
               csv.DictReader((HERE / "adjudication_dossier.csv").open(encoding="utf-8-sig", newline=""))}
    adj = json.loads((HERE / "adjudication_checkpoint.json").read_text(encoding="utf-8"))

    cases = []
    for pid, row in dossier.items():
        a = adj.get(pid)
        first, second = ids(row["first_ids"]), ids(row["second_ids"])
        packet = ids(row["candidate_ids_in_packet"]) | ids(row["retrieved_extra_author_ids"])
        if not a:
            cases.append({"person_id": pid, "adjudicated": False})
            continue
        final = ids(a["adjudicated_ids"])
        st = a["adjudicated_status"]
        both_verified = row["first_status"] in VERIFIED and row["second_status"] in VERIFIED
        # Inclusion-set relations are only meaningful where both sides asserted an identity.
        relation = "not_applicable"
        if both_verified:
            union, inter = first | second, first & second
            if final == first and final == second:
                relation = "identical"
            elif final >= union and final != union:
                relation = "broader_than_both"
            elif final == union:
                relation = "union_of_both"
            elif final <= inter:
                relation = "narrower_than_both"
            elif final <= union:
                relation = "within_union_mixed"
            else:
                relation = "partially_outside_reviews"
        cases.append({
            "person_id": pid,
            "adjudicated": True,
            "name": row["canonical_name"],
            "disagreement_type": row["disagreement_type"],
            "first_status": row["first_status"],
            "second_status": row["second_status"],
            "adjudicated_status": st,
            "n_first_ids": len(first),
            "n_second_ids": len(second),
            "n_final_ids": len(final),
            "ids_not_in_packet": sorted(final - packet),
            "dropped_ids_invented_by_model": a.get("invented_ids_dropped", ""),
            "set_relation_to_reviews": relation,
            "adopts_first_exactly": final == first and st == row["first_status"],
            "adopts_second_exactly": final == second and st == row["second_status"],
            "neither_side_exactly": not (
                (final == first and st == row["first_status"])
                or (final == second and st == row["second_status"])
            ),
            "retrieval_needed": a.get("retrieval_needed"),
            "retrieval_spec": a.get("retrieval_spec", ""),
            "normalization_note": a.get("normalization_note", ""),
        })

    done = [c for c in cases if c["adjudicated"]]
    summary = {
        "cases_in_dossier": len(cases),
        "adjudicated": len(done),
        "outstanding": sorted(c["person_id"] for c in cases if not c["adjudicated"]),
        "final_status_distribution": {},
        "set_relation_distribution": {},
        "adopted_first_verdict_exactly": sum(1 for c in done if c["adopts_first_exactly"]),
        "adopted_second_verdict_exactly": sum(1 for c in done if c["adopts_second_exactly"]),
        "blend_or_novel_verdict": sum(1 for c in done if c["neither_side_exactly"]),
        "broader_than_both_reviews": sum(1 for c in done if c["set_relation_to_reviews"] == "broader_than_both"),
        "narrower_than_both_reviews": sum(1 for c in done if c["set_relation_to_reviews"] == "narrower_than_both"),
        "union_of_both_reviews": sum(1 for c in done if c["set_relation_to_reviews"] == "union_of_both"),
        "ungrounded_included_ids": {
            c["person_id"]: c["ids_not_in_packet"] for c in done if c["ids_not_in_packet"]
        },
        "invented_ids_dropped": {
            c["person_id"]: c["dropped_ids_invented_by_model"] for c in done
            if c["dropped_ids_invented_by_model"]
        },
        "flagged_for_additional_retrieval": sorted(
            c["person_id"] for c in done if c["retrieval_needed"]
        ),
        "normalization_notes": {
            c["person_id"]: c["normalization_note"] for c in done if c["normalization_note"]
        },
        "total_included_ids": sum(c["n_final_ids"] for c in done),
    }
    for c in done:
        summary["final_status_distribution"][c["adjudicated_status"]] = (
            summary["final_status_distribution"].get(c["adjudicated_status"], 0) + 1
        )
        summary["set_relation_distribution"][c["set_relation_to_reviews"]] = (
            summary["set_relation_distribution"].get(c["set_relation_to_reviews"], 0) + 1
        )

    (HERE / "adjudication_audit_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    with (HERE / "adjudication_audit_cases.csv").open("w", encoding="utf-8", newline="") as fh:
        keys = ["person_id", "name", "disagreement_type", "adjudicated", "first_status",
                "second_status", "adjudicated_status", "n_first_ids", "n_second_ids",
                "n_final_ids", "set_relation_to_reviews", "adopts_first_exactly",
                "adopts_second_exactly", "retrieval_needed", "retrieval_spec",
                "ids_not_in_packet", "normalization_note"]
        w = csv.DictWriter(fh, fieldnames=keys, lineterminator="\n")
        w.writeheader()
        for c in cases:
            w.writerow({k: (";".join(c[k]) if isinstance(c.get(k), list) else c.get(k, "")) for k in keys})
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
