#!/usr/bin/env python3
"""Ingest a raw blinded GPTPage Coder B response into validated ARIS4C003 files.

Expected raw response:
- exactly one fenced CSV block with header
  concept_id,discipline,D1,...,D11,IKES_B
- evidence notes outside that block;
- a BLINDING DECLARATION section containing exactly
  INDEPENDENCE_STATUS: PASS
  for an admissible independent second coding pass.

This script does not adjudicate disagreements and never reads contemporary
research outcomes.
"""

from __future__ import annotations

import argparse
import csv
import io
import math
import re
from pathlib import Path

import pandas as pd

DIMS = [f"D{i}" for i in range(1, 12)]
EXPECTED_IDS = [f"D{i:02d}" for i in range(1, 22)]
EXPECTED_HEADER = ["concept_id", "discipline", *DIMS, "IKES_B"]


def extract_csv_block(text: str) -> tuple[str, tuple[int, int]]:
    matches = list(
        re.finditer(
            r"(?ims)^[ \t]*```csv[ \t]*\n(.*?)^[ \t]*```[ \t]*$",
            text,
        )
    )
    if len(matches) != 1:
        raise SystemExit(
            f"Expected exactly one fenced CSV block, found {len(matches)}"
        )
    m = matches[0]
    return m.group(1).strip() + "\n", m.span()


def parse_score(value: object, label: str) -> float | None:
    if value is None:
        return None
    s = str(value).strip()
    if s == "" or s.upper() == "NA":
        return None
    try:
        x = float(s)
    except ValueError as exc:
        raise SystemExit(f"{label}: invalid score {value!r}") from exc
    if x < 0 or x > 3:
        raise SystemExit(f"{label}: score outside 0-3: {x}")
    if not math.isclose(x, round(x), abs_tol=1e-12):
        raise SystemExit(f"{label}: D1-D11 scores must be integer 0,1,2,3 or NA")
    return float(round(x))


def validate_matrix(csv_text: str) -> pd.DataFrame:
    reader = csv.reader(io.StringIO(csv_text))
    rows = list(reader)
    if not rows:
        raise SystemExit("Coder B CSV is empty")
    header = [x.strip() for x in rows[0]]
    if header != EXPECTED_HEADER:
        raise SystemExit(
            "Coder B CSV header differs from frozen schema.\n"
            f"Expected: {EXPECTED_HEADER}\nGot: {header}"
        )

    df = pd.read_csv(io.StringIO(csv_text), dtype=str, keep_default_na=False)
    if len(df) != 21:
        raise SystemExit(f"Expected 21 Coder B rows, found {len(df)}")
    if df["concept_id"].tolist() != EXPECTED_IDS:
        raise SystemExit(
            "Coder B concept_id order must be exactly D01-D21; "
            f"got {df['concept_id'].tolist()}"
        )
    if df["concept_id"].duplicated().any():
        raise SystemExit("Duplicate concept_id in Coder B matrix")

    numeric: dict[str, list[float | None]] = {d: [] for d in DIMS}
    for idx, row in df.iterrows():
        cid = row["concept_id"]
        for d in DIMS:
            numeric[d].append(parse_score(row[d], f"{cid}/{d}"))

    out = df[["concept_id", "discipline"]].copy()
    for d in DIMS:
        out[d] = numeric[d]

    provided = pd.to_numeric(df["IKES_B"].replace({"": pd.NA, "NA": pd.NA}), errors="coerce")
    recomputed = out[DIMS].mean(axis=1, skipna=True)

    # Every discipline needs at least one score, and provided IKES_B must match
    # the mean of available dimensions to rounding tolerance.
    if out[DIMS].notna().sum(axis=1).eq(0).any():
        bad = out.loc[out[DIMS].notna().sum(axis=1).eq(0), "concept_id"].tolist()
        raise SystemExit(f"No scored IKES dimensions for: {bad}")
    if provided.isna().any():
        bad = df.loc[provided.isna(), "concept_id"].tolist()
        raise SystemExit(f"IKES_B missing/non-numeric for: {bad}")

    mismatch = (provided.astype(float) - recomputed).abs() > 0.011
    if mismatch.any():
        details = pd.DataFrame(
            {
                "concept_id": df.loc[mismatch, "concept_id"],
                "provided_IKES_B": provided.loc[mismatch].astype(float),
                "recomputed_IKES_B": recomputed.loc[mismatch],
            }
        )
        raise SystemExit(
            "IKES_B does not equal the mean of available D1-D11 scores:\n"
            + details.to_string(index=False)
        )

    out["IKES_B"] = recomputed
    return out


def validate_evidence_sections(text_without_csv: str) -> None:
    heading_re = re.compile(
        r"(?m)^###\s+(D\d{2})\s+—\s+.+$"
    )
    matches = list(heading_re.finditer(text_without_csv))
    ids = [m.group(1) for m in matches]
    if ids != EXPECTED_IDS:
        missing = [cid for cid in EXPECTED_IDS if cid not in ids]
        extras = [cid for cid in ids if cid not in EXPECTED_IDS]
        raise SystemExit(
            "Coder B evidence headings must appear exactly once and in D01-D21 "
            f"order. Missing={missing}; extras={extras}; observed={ids}"
        )

    blinding_pos = text_without_csv.find("BLINDING DECLARATION")
    for idx, match in enumerate(matches):
        cid = match.group(1)
        end = (
            matches[idx + 1].start()
            if idx + 1 < len(matches)
            else (blinding_pos if blinding_pos >= 0 else len(text_without_csv))
        )
        section = text_without_csv[match.end() : end]
        confidence = re.findall(
            r"(?mi)^Confidence:\s*(high|medium|low)\s*$",
            section,
        )
        if len(confidence) != 1:
            raise SystemExit(
                f"{cid}: expected exactly one Confidence: high/medium/low line"
            )
        prose = re.sub(r"(?mi)^Confidence:.*$", "", section).strip()
        if len(prose) < 80:
            raise SystemExit(
                f"{cid}: evidence section is too short to satisfy the frozen "
                "historical-rationale requirement"
            )


def validate_blinding(text: str) -> None:
    if "BLINDING DECLARATION" not in text:
        raise SystemExit("Missing BLINDING DECLARATION section")

    bundle_pass = len(re.findall(r"(?m)^BUNDLE_ACCESS_STATUS:\s*PASS\s*$", text))
    bundle_fail = len(re.findall(r"(?m)^BUNDLE_ACCESS_STATUS:\s*FAIL\s*$", text))
    if bundle_fail:
        raise SystemExit(
            "Coder B declared BUNDLE_ACCESS_STATUS: FAIL; this response cannot "
            "serve as the confirmatory independent coding pass."
        )
    if bundle_pass != 1:
        raise SystemExit(
            "Expected exactly one line 'BUNDLE_ACCESS_STATUS: PASS' under "
            "BLINDING DECLARATION."
        )

    pass_count = len(re.findall(r"(?m)^INDEPENDENCE_STATUS:\s*PASS\s*$", text))
    fail_count = len(re.findall(r"(?m)^INDEPENDENCE_STATUS:\s*FAIL\s*$", text))
    if fail_count:
        raise SystemExit(
            "Coder B declared INDEPENDENCE_STATUS: FAIL; this response cannot "
            "serve as the confirmatory independent coding pass."
        )
    if pass_count != 1:
        raise SystemExit(
            "Expected exactly one line 'INDEPENDENCE_STATUS: PASS' under "
            "BLINDING DECLARATION."
        )


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("raw_response", type=Path)
    p.add_argument("--output-csv", type=Path, required=True)
    p.add_argument("--output-notes", type=Path, required=True)
    args = p.parse_args()

    text = args.raw_response.read_text(encoding="utf-8")
    validate_blinding(text)
    csv_text, span = extract_csv_block(text)
    df = validate_matrix(csv_text)
    non_csv_text = text[: span[0]] + text[span[1] :]
    validate_evidence_sections(non_csv_text)

    # Preserve the complete non-CSV evidence narrative, including the blinding
    # declaration, and record the raw-response path without rewriting claims.
    notes = (
        "# IKES CODER B — EVIDENCE NOTES\n\n"
        f"Raw GPTPage response: `{args.raw_response}`\n\n"
        + non_csv_text.strip()
        + "\n"
    )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    args.output_notes.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output_csv, index=False, float_format="%.6f")
    args.output_notes.write_text(notes, encoding="utf-8")

    na_cells = int(df[DIMS].isna().sum().sum())
    print(
        {
            "status": "PASS",
            "disciplines": len(df),
            "dimension_cells": len(df) * len(DIMS),
            "na_cells_requiring_adjudication": na_cells,
            "output_csv": str(args.output_csv),
            "output_notes": str(args.output_notes),
        }
    )


if __name__ == "__main__":
    main()
