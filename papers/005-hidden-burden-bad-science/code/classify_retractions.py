#!/usr/bin/env python3
"""Derive conservative ARIS4C005 exposure flags from Retraction Watch reasons.

This script is intentionally conservative. It preserves every raw reason and
adds screening flags; ambiguous rows remain manual-review candidates rather
than being forced into a misconduct label.

It is NOT a substitute for reading the notice or adjudicating intent.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Iterable

# High-specificity severe scientific integrity evidence.
E1S_NARROW = {
    "Falsification/Fabrication of Data",
    "Falsification/Fabrication of Image",
    "Falsification/Fabrication of Results",
}

# Strong process/organized integrity signals. Scientific unreliability may still
# require contextual confirmation.
E1P_STRONG = {
    "Paper Mill",
    "False/Forged Authorship",
    "False/Forged Affiliation",
    "Rogue Editor",
    "Hoax Paper",
}

# Confirmed/strong misconduct families that may not invalidate substantive data.
E1M_STRONG = {
    *E1S_NARROW,
    "Plagiarism of/in Article",
    "Plagiarism of Data",
    "Plagiarism of Image",
    "Plagiarism of Text",
    "Taken via Peer Review",
    "Paper Mill",
    "False/Forged Authorship",
    "False/Forged Affiliation",
}

# Material unreliability / research-waste signals that do not establish intent.
E3_ERROR = {
    "Error in Analyses",
    "Error in Cell Lines/Tissues",
    "Error in Data",
    "Error in Image",
    "Error in Materials",
    "Error in Methods",
    "Error in Results and/or Conclusions",
    "Contamination of Cell Lines/Tissues",
    "Contamination of Materials",
    "Results Not Reproducible",
}

# Reasons needing notice/context review before E1-S assignment.
MANUAL_SCIENTIFIC_REVIEW = {
    "Manipulation of Data.",
    "Manipulation of Images",
    "Manipulation of Results",
    "Unreliable Data",
    "Unreliable Image",
    "Unreliable Results and/or Conclusions",
    "Original Data and/or Images not Provided and/or not Available",
    "Concerns/Issues About Data",
    "Concerns/Issues About Image",
    "Concerns/Issues about Results and/or Conclusions",
    "Euphemisms for Misconduct",
    "Ethical Violations by Author",
}

# Discovery/context reasons: never sufficient by themselves for misconduct.
CONTEXT_ONLY = {
    "Author Unresponsive",
    "Concerns/Issues about Article",
    "Investigation by Company/Institution",
    "Investigation by Journal/Publisher",
    "Investigation by ORI",
    "Investigation by Third Party",
    "Objections by Author(s)",
    "Objections by Company/Institution",
    "Objections by Third Party",
    "Legal Reasons and/or Threats",
    "Conflict of Interest",
    "Breach of Policy by Author",
}

REASON_COLUMN_CANDIDATES = (
    "Reason(s) for Retraction",
    "Reason",
    "Reasons",
    "reason",
    "reasons",
)


def split_reasons(raw: str | None) -> list[str]:
    """Split Retraction Watch's semicolon-separated reason list."""
    if not raw:
        return []
    return [part.strip() for part in raw.split(";") if part.strip()]


def any_in(reasons: Iterable[str], vocabulary: set[str]) -> bool:
    return any(reason in vocabulary for reason in reasons)


def classify(reasons: list[str]) -> dict[str, int]:
    reason_set = set(reasons)
    e1s_narrow = bool(reason_set & E1S_NARROW)
    paper_mill = "Paper Mill" in reason_set
    e1m_strong = bool(reason_set & E1M_STRONG)
    e1p_strong = bool(reason_set & E1P_STRONG)
    e3_error = bool(reason_set & E3_ERROR)
    manual_scientific = bool(reason_set & MANUAL_SCIENTIFIC_REVIEW)
    context_only = bool(reason_set) and reason_set.issubset(CONTEXT_ONLY)

    # Broad E1-S is deliberately *not* assigned automatically from ambiguous
    # unreliability/manipulation labels. It equals narrow here and is intended
    # to be updated after notice/manual adjudication downstream.
    return {
        "e1s_narrow_auto": int(e1s_narrow),
        "e1m_strong_auto": int(e1m_strong),
        "e1p_strong_auto": int(e1p_strong),
        "paper_mill_signal": int(paper_mill),
        "e3_error_signal": int(e3_error),
        "manual_scientific_review": int(manual_scientific),
        "context_only_reasons": int(context_only),
        "manual_review_required": int(
            manual_scientific
            or context_only
            or (e1p_strong and not e1s_narrow)
            or not reasons
        ),
    }


def detect_reason_column(fieldnames: list[str] | None) -> str:
    if not fieldnames:
        raise ValueError("Input CSV has no header")
    for candidate in REASON_COLUMN_CANDIDATES:
        if candidate in fieldnames:
            return candidate
    raise ValueError(
        "Could not find a reasons column. Use --reason-column. "
        f"Available columns: {fieldnames}"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--reason-column")
    args = parser.parse_args()

    with args.input_csv.open("r", encoding="utf-8-sig", newline="") as src:
        reader = csv.DictReader(src)
        reason_column = args.reason_column or detect_reason_column(reader.fieldnames)
        flag_names = list(classify([]).keys())
        output_fields = list(reader.fieldnames or []) + [
            "aris_raw_reason_count",
            *flag_names,
        ]

        args.output_csv.parent.mkdir(parents=True, exist_ok=True)
        with args.output_csv.open("w", encoding="utf-8", newline="") as dst:
            writer = csv.DictWriter(dst, fieldnames=output_fields)
            writer.writeheader()
            for row in reader:
                reasons = split_reasons(row.get(reason_column))
                row["aris_raw_reason_count"] = len(reasons)
                row.update(classify(reasons))
                writer.writerow(row)

    print(f"Wrote classified Retraction Watch rows to {args.output_csv}")
    print(
        "Reminder: *_auto flags are screening variables. "
        "Ambiguous rows require notice/manual adjudication."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
