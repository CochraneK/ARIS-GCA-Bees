#!/usr/bin/env python3
"""Guard raw OpenAlex fragment-pair evidence against false support labels.

The upstream collector deliberately exposes transparent evidence and a loose
review-priority score. This module adds the stricter epistemic rule used by the
canonical identity workflow: a pair cannot be called `support` merely because a
few weak contextual similarities add up to enough points.

A strong identity anchor requires at least one of:
- same non-empty ORCID;
- duplicate DOI inside the candidate-lifetime window;
- normalized-title overlap inside that window;
- >=2 shared coauthors with overlap coefficient >=0.25;
- shared institution + topic Jaccard >=0.25 + >=1 shared coauthor.

The guard never turns `needs_review` into `support`; it only preserves or
downgrades support, and it never overrides an explicit conflict.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def as_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def as_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def has_strong_identity_anchor(row: dict[str, Any]) -> tuple[bool, list[str]]:
    anchors: list[str] = []

    if bool(row.get("same_orcid")):
        anchors.append("same_nonempty_orcid")
    if as_int(row.get("lifetime_doi_overlap_n")) > 0:
        anchors.append("lifetime_duplicate_doi")
    if as_int(row.get("lifetime_title_overlap_n")) > 0:
        anchors.append("lifetime_normalized_title_overlap")

    shared_coauthors = as_int(row.get("lifetime_shared_coauthors_n"))
    coauthor_overlap = as_float(row.get("lifetime_coauthor_overlap_coefficient"))
    if shared_coauthors >= 2 and coauthor_overlap is not None and coauthor_overlap >= 0.25:
        anchors.append("high_proportion_shared_coauthors")

    shared_institutions = as_int(row.get("lifetime_shared_institutions_n"))
    topic_jaccard = as_float(row.get("lifetime_topic_jaccard"))
    if (
        shared_institutions >= 1
        and shared_coauthors >= 1
        and topic_jaccard is not None
        and topic_jaccard >= 0.25
    ):
        anchors.append("institution_topic_coauthor_convergence")

    return bool(anchors), anchors


def guard_pair_evidence(row: dict[str, Any]) -> dict[str, Any]:
    guarded = dict(row)
    raw_label = str(row.get("review_label") or "needs_review")
    strong_anchor, anchors = has_strong_identity_anchor(row)

    guarded["raw_review_label"] = raw_label
    guarded["strong_identity_anchor"] = strong_anchor
    guarded["identity_anchor_reasons"] = anchors

    conflict_reasons = list(row.get("conflict_reasons") or [])
    if raw_label == "conflict" or conflict_reasons:
        guarded["guarded_review_label"] = "conflict"
        guarded["guard_action"] = "preserve_conflict"
        return guarded

    if raw_label == "support" and not strong_anchor:
        guarded["guarded_review_label"] = "needs_review"
        guarded["guard_action"] = "downgrade_weak_context_only_support"
        return guarded

    if raw_label == "support" and strong_anchor:
        guarded["guarded_review_label"] = "support"
        guarded["guard_action"] = "preserve_support_with_anchor"
        return guarded

    # The guard cannot promote uncertain raw evidence.
    guarded["guarded_review_label"] = "needs_review"
    guarded["guard_action"] = "preserve_needs_review"
    return guarded


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("pairwise_jsonl", type=Path)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    args = parser.parse_args()

    rows = [
        json.loads(line)
        for line in args.pairwise_jsonl.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    guarded_rows = [guard_pair_evidence(row) for row in rows]

    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with args.output_jsonl.open("w", encoding="utf-8") as handle:
        for row in guarded_rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    raw_counts = {"support": 0, "conflict": 0, "needs_review": 0}
    guarded_counts = {"support": 0, "conflict": 0, "needs_review": 0}
    downgraded = 0
    for row in guarded_rows:
        raw = row["raw_review_label"]
        final = row["guarded_review_label"]
        raw_counts[raw] = raw_counts.get(raw, 0) + 1
        guarded_counts[final] = guarded_counts.get(final, 0) + 1
        if raw == "support" and final != "support":
            downgraded += 1

    summary = {
        "pair_n": len(guarded_rows),
        "raw_label_counts": raw_counts,
        "guarded_label_counts": guarded_counts,
        "weak_support_pairs_downgraded": downgraded,
        "strong_anchor_support_pairs": sum(
            row["guarded_review_label"] == "support" for row in guarded_rows
        ),
        "policy": (
            "Canonical identity review uses guarded labels. Weak contextual overlap "
            "cannot independently establish fragment support, and the guard never "
            "promotes needs_review to support."
        ),
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
