#!/usr/bin/env python3
"""Classify DAIS-C text assets without emitting interview content.

This script identifies structural file classes using the public DAIS-C transcription
conventions. It outputs aggregate counts only; participant IDs and transcript text are
never written to the repository.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

TEXT_EXTENSIONS = {".txt", ".rtf"}
PARTICIPANT_BLOCK = re.compile(
    r"<([0-9]{2}[A-Z]{2}[0-9]{2})>(.*?)</\1>", re.DOTALL
)
INT_BLOCK = re.compile(r"<INT>(.*?)</INT>", re.DOTALL | re.IGNORECASE)
TIMESTAMP = re.compile(r"#\d{2}:\d{2}:\d{2}(?:[-.]\d+)?#")
XML_TAG = re.compile(r"<[^>]+>")
WORD = re.compile(r"\b[\w'-]+\b", re.UNICODE)


def safe_read(path: Path) -> str | None:
    for enc in ("utf-8", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
        except Exception:
            return None
    return None


def clean_words(text: str) -> int:
    text = XML_TAG.sub(" ", text)
    text = re.sub(r"\\[A-Za-z]+-?\d* ?", " ", text)  # common RTF control words
    text = text.replace("{", " ").replace("}", " ")
    return len(WORD.findall(text))


def classify(text: str) -> tuple[str, int, int, int]:
    participant_blocks = PARTICIPANT_BLOCK.findall(text)
    int_blocks = INT_BLOCK.findall(text)
    timestamps = len(TIMESTAMP.findall(text))
    participant_words = sum(clean_words(block) for _, block in participant_blocks)
    interviewer_words = sum(clean_words(block) for block in int_blocks)

    if timestamps >= 3 and participant_blocks:
        kind = "timestamped"
    elif participant_blocks and int_blocks and participant_words >= 50:
        kind = "interactional"
    elif participant_blocks and not int_blocks and participant_words >= 50:
        kind = "speaker_only"
    elif participant_blocks:
        kind = "participant_tagged_other"
    else:
        kind = "non_transcript_text"
    return kind, participant_words, interviewer_words, timestamps


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--md-out", required=True)
    args = ap.parse_args()

    root = Path(args.root)
    counts = Counter()
    ext_by_kind: dict[str, Counter] = defaultdict(Counter)
    participant_words = Counter()
    interviewer_words = Counter()
    timestamp_counts = Counter()
    unique_ids_by_kind: dict[str, set[str]] = defaultdict(set)

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = safe_read(path)
        if text is None:
            continue
        kind, pwords, iwords, ts = classify(text)
        counts[kind] += 1
        ext_by_kind[kind][path.suffix.lower()] += 1
        participant_words[kind] += pwords
        interviewer_words[kind] += iwords
        timestamp_counts[kind] += ts
        for pid, _ in PARTICIPANT_BLOCK.findall(text):
            unique_ids_by_kind[kind].add(pid)

    result = {
        "dataset": "DAIS-C",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "privacy_rule": "No transcript text or participant IDs emitted.",
        "classification_counts": dict(sorted(counts.items())),
        "extensions_by_class": {
            k: dict(sorted(v.items())) for k, v in sorted(ext_by_kind.items())
        },
        "participant_word_counts_by_class": dict(sorted(participant_words.items())),
        "interviewer_word_counts_by_class": dict(sorted(interviewer_words.items())),
        "timestamp_markers_by_class": dict(sorted(timestamp_counts.items())),
        "unique_participant_id_counts_by_class": {
            k: len(v) for k, v in sorted(unique_ids_by_kind.items())
        },
        "published_reference": {
            "paper_total_tokens": 97357,
            "paper_audio_minutes": 1284.8,
            "note": (
                "Published token count is a validation reference, not an expected exact "
                "match because tokenization and file class differ."
            ),
        },
    }

    jout = Path(args.json_out)
    mout = Path(args.md_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    mout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    rows = []
    for kind in sorted(counts):
        rows.append(
            f"| {kind} | {counts[kind]} | "
            f"{len(unique_ids_by_kind[kind])} | "
            f"{participant_words[kind]:,} | "
            f"{interviewer_words[kind]:,} |"
        )

    md = f"""# ARIS4C009 Pilot-0 · DAIS-C structural classification

**Generated:** {result['generated_utc']}

## Privacy rule

No transcript text or participant IDs are emitted. Classification occurs only inside
the transient GitHub Actions runner.

## Structural classes

| Class | Files | Unique pseudonymous speaker IDs | Participant words | Interviewer words |
|---|---:|---:|---:|---:|
{chr(10).join(rows)}

## Published validation reference

The DAIS-C resource paper reports approximately:

- 97,357 corpus tokens;
- 1,284.8 audio minutes.

Those values are **not** expected to match this script exactly because the archive
contains multiple representations of the same speech and the script uses a simple
Unicode word tokenizer. They are used to detect gross duplication or parser failure.

## Canonical-candidate rule

For Pilot-0 episode parsing, the preferred source class is:

> `interactional` — files containing both a participant XML block and `<INT>`
> interviewer blocks, while excluding timestamp-only representations.

If this class does not recover approximately one transcript representation per
participant or produces implausible aggregate scale, the parser must be revised before
any fidelity analysis.

## Next gate

Freeze an episode parser on calibration-only files and report only aggregate episode
counts, length distributions, and annotation feasibility before manual fidelity scoring.
"""
    mout.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
