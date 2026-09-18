#!/usr/bin/env python3
"""Audit the 1988 NVSS/NBER mortality layout before ARIS4C013 Pilot 0.

This script intentionally does not analyze mortality outcomes.  It only asks
whether the source layout exposes enough date precision to support the planned
birth–death phase and birthday-window analyses.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

DATE_WORDS = re.compile(r"\b(date|day|month|year)\b", re.I)
BIRTH_WORDS = re.compile(r"\b(birth|born|dob)\b|brth|bday", re.I)
DEATH_WORDS = re.compile(r"\b(death|died|dod)\b|dth|dday", re.I)

BIRTH_DAY_PATTERNS = [
    re.compile(p, re.I)
    for p in (
        r"day\s+of\s+birth",
        r"birth\s+day",
        r"date\s+of\s+birth",
        r"\bbday\b",
        r"(?:birth|brth|dob).{0,20}(?:day|date)",
        r"(?:day|date).{0,20}(?:birth|brth)",
    )
]
DEATH_DAY_PATTERNS = [
    re.compile(p, re.I)
    for p in (
        r"day\s+of\s+death",
        r"death\s+day",
        r"date\s+of\s+death",
        r"\bdday\b",
        r"(?:death|dth|dod).{0,20}(?:day|date)",
        r"(?:day|date).{0,20}(?:death|dth)",
    )
]

def matching_lines(text: str) -> list[str]:
    out = []
    for raw in text.splitlines():
        line = " ".join(raw.split())
        if not line:
            continue
        if DATE_WORDS.search(line) or BIRTH_WORDS.search(line) or DEATH_WORDS.search(line):
            out.append(line)
    return out

def has_any(lines: list[str], patterns: list[re.Pattern[str]]) -> bool:
    return any(p.search(line) for line in lines for p in patterns)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dct", type=Path, required=True)
    ap.add_argument("--do", dest="do_file", type=Path)
    ap.add_argument("--json-out", type=Path)
    args = ap.parse_args()

    dct = args.dct.read_text(encoding="utf-8", errors="replace")
    do_text = args.do_file.read_text(encoding="utf-8", errors="replace") if args.do_file and args.do_file.exists() else ""
    combined = dct + "\n" + do_text
    lines = matching_lines(combined)

    birth_day = has_any(lines, BIRTH_DAY_PATTERNS)
    death_day = has_any(lines, DEATH_DAY_PATTERNS)
    result = {
        "source": str(args.dct),
        "candidate_lines": lines,
        "birth_exact_day_candidate": birth_day,
        "death_exact_day_candidate": death_day,
        "pilot0_exact_date_gate": bool(birth_day and death_day),
        "interpretation": (
            "PASS: layout text contains candidates for both exact birth-day and death-day fields."
            if birth_day and death_day
            else "BLOCKED: do not run exact-date Pilot 0 until missing field(s) are verified in the original layout."
        ),
    }

    print("# ARIS4C013 · NVSS 1988 field audit")
    print()
    print(f"- birth exact-day candidate: **{birth_day}**")
    print(f"- death exact-day candidate: **{death_day}**")
    print(f"- exact-date Pilot 0 gate: **{'PASS' if result['pilot0_exact_date_gate'] else 'BLOCKED'}**")
    print()
    print("## Candidate layout lines")
    for line in lines[:250]:
        print(f"- {line}")
    if len(lines) > 250:
        print(f"- ... {len(lines) - 250} additional candidate lines omitted from log")

    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # A blocked gate is a scientific result of the audit, not a CI infrastructure failure.
    # Exit 0 so the artifact is still uploaded and can be reviewed.
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
