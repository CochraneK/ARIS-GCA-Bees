#!/usr/bin/env python3
"""Derive conservative ARIS4C005 exposure flags from Retraction Watch reasons.

This script is intentionally conservative. It preserves every raw reason and
adds screening flags; ambiguous rows remain manual-review candidates rather
than being forced into a misconduct label.

Reason matching is case/whitespace-insensitive because Retraction Watch has
renamed and normalized reason labels over time. It is NOT a substitute for
reading the notice or adjudicating intent.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def normalize_reason(value: str) -> str:
    return " ".join(value.strip().split()).casefold()


def vocab(*values: str) -> set[str]:
    return {normalize_reason(value) for value in values}


# High-specificity severe scientific integrity evidence. Retraction Watch's
# current guide defines these as fabrication/falsification in order to mislead.
E1S_NARROW = vocab(
    "Falsification/Fabrication of Data",
    "Falsification/Fabrication of Image",
    "Falsification/Fabrication of Results",
)

# Strong publication-process/organized-integrity signals. Scientific
# unreliability may still require contextual confirmation.
E1P_STRONG = vocab(
    "Paper Mill",
    "False/Forged Authorship",
    "False/Forged Affiliation",
    "Rogue Editor",
    "Hoax Paper",
    "Compromised Peer Review",
    # Historical label retained for old snapshots.
    "Fake Peer Review",
)

# Strong misconduct/integrity-violation families that may not invalidate the
# substantive scientific result. Compromised Peer Review is deliberately not
# here because Retraction Watch removed intentionality from its definition in
# Dec 2025.
E1M_STRONG = E1S_NARROW | vocab(
    "Plagiarism of/in Article",
    "Plagiarism of Data",
    "Plagiarism of Image",
    "Plagiarism of Text",
    "Euphemisms for Plagiarism",
    "Euphemisms for Misconduct",
    "Taken via Peer Review",
    "Paper Mill",
    "False/Forged Authorship",
    "False/Forged Affiliation",
)

# Material unreliability / research-waste signals that do not establish intent.
E3_ERROR = vocab(
    "Error in Analyses",
    "Error in Cell Lines/Tissues",
    "Error in Data",
    "Error in Image",
    "Error in Materials",
    "Error in Methods",
    "Error in Results and/or Conclusions",
    "Error in Text",
    "Contamination of Cell Lines/Tissues",
    "Contamination of Materials",
    "Results Not Reproducible",
)

# Reasons needing notice/context review before severe scientific-unreliability
# assignment. These indicate possible scientific unreliability but do not by
# themselves establish fabrication/falsification or intent.
MANUAL_SCIENTIFIC_REVIEW = vocab(
    "Manipulation of Data",
    "Manipulation of Data.",
    "Manipulation of Images",
    "Manipulation of Results",
    "Unreliable Data",
    "Unreliable Image",
    "Unreliable Results and/or Conclusions",
    "Original Data and/or Images not Provided and/or not Available",
    "Concerns/Issues about Data",
    "Concerns/Issues about Image",
    "Concerns/Issues about Results and/or Conclusions",
    "Concerns/Issues about Methods",
    "Computer-Aided Content or Computer-Generated Content",
    "Hoax Paper",
)

# Reasons that can indicate a publication/research-integrity process problem but
# need context before a stronger label. This keeps procedural concerns distinct
# from scientific unreliability.
MANUAL_PROCESS_REVIEW = vocab(
    "Concerns/Issues about Peer Review",
    "Concerns/Issues with Peer Review",
    "Concerns/Issues about Referencing/Attributions",
    "Concerns/Issues about Authorship/Affiliation",
    "Concerns/Issues about Third Party Involvement",
    "Breach of Policy by Author",
    "Conflict of Interest",
    "Lack of IRB/IACUC Approval and/or Compliance",
    "Informed/Patient Consent – None/Withdrawn",
    "Informed/Patient Consent - None/Withdrawn",
    "Computer-Aided Content or Computer-Generated Content",
)

# Discovery/context reasons: never sufficient by themselves for misconduct.
CONTEXT_ONLY = vocab(
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
    "Notice - Limited or No Information",
    "Notice – Unable to Access via current resources",
    "Date of Article and/or Notice Unknown",
)

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


def classify(reasons: list[str]) -> dict[str, int]:
    reason_set = {normalize_reason(reason) for reason in reasons}
    e1s_narrow = bool(reason_set & E1S_NARROW)
    paper_mill = normalize_reason("Paper Mill") in reason_set
    e1m_strong = bool(reason_set & E1M_STRONG)
    e1p_strong = bool(reason_set & E1P_STRONG)
    e3_error = bool(reason_set & E3_ERROR)
    manual_scientific = bool(reason_set & MANUAL_SCIENTIFIC_REVIEW)
    manual_process = bool(reason_set & MANUAL_PROCESS_REVIEW)
    context_only = bool(reason_set) and reason_set.issubset(CONTEXT_ONLY)

    # Broad E1-S is deliberately *not* assigned automatically from ambiguous
    # unreliability/manipulation labels. It is created only after notice/manual
    # adjudication downstream.
    return {
        "e1s_narrow_auto": int(e1s_narrow),
        "e1m_strong_auto": int(e1m_strong),
        "e1p_strong_auto": int(e1p_strong),
        "paper_mill_signal": int(paper_mill),
        "e3_error_signal": int(e3_error),
        "manual_scientific_review": int(manual_scientific),
        "manual_process_review": int(manual_process),
        "context_only_reasons": int(context_only),
        "manual_review_required": int(
            manual_scientific
            or manual_process
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
