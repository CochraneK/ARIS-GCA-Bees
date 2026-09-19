#!/usr/bin/env python3
"""Build a privacy-preserving episode inventory from DAIS-C interactional transcripts.

No transcript text, file names, or participant IDs are emitted. The output contains
only cohort-level and whole-corpus structural statistics used to decide whether
ARIS4C009 Pilot-0 can proceed to human annotation.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import re
import statistics
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

BLOCK = re.compile(
    r"<(INT|[0-9]{2}[A-Z]{2,3}[0-9]{2})>(.*?)</\1>",
    re.DOTALL | re.IGNORECASE,
)
TIMESTAMP = re.compile(r"#\d{2}:\d{2}:\d{2}(?:[-.]\d+)?#")
XML_TAG = re.compile(r"<[^>]+>")
WORD = re.compile(r"\b[\w'-]+\b", re.UNICODE)
RTF_CONTROL = re.compile(r"\\[A-Za-z]+-?\d* ?")


def read_docx(path: Path) -> str | None:
    try:
        with zipfile.ZipFile(path) as zf:
            raw = zf.read("word/document.xml")
        root = ET.fromstring(raw)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
        paras = []
        for p in root.findall(".//w:p", ns):
            pieces = []
            for node in p.iter():
                if node.tag.endswith("}t") and node.text:
                    pieces.append(node.text)
                elif node.tag.endswith("}tab"):
                    pieces.append("\t")
                elif node.tag.endswith("}br"):
                    pieces.append("\n")
            if pieces:
                paras.append("".join(pieces))
        return "\n".join(paras)
    except Exception:
        return None


def read_text(path: Path) -> str | None:
    if path.suffix.lower() == ".docx":
        return read_docx(path)
    for enc in ("utf-8", "latin-1"):
        try:
            return html.unescape(path.read_text(encoding=enc))
        except UnicodeDecodeError:
            continue
        except Exception:
            return None
    return None


def clean_word_count(text: str) -> int:
    text = XML_TAG.sub(" ", text)
    text = RTF_CONTROL.sub(" ", text)
    text = text.replace("{", " ").replace("}", " ")
    return len(WORD.findall(text))


def cohort_for(path: Path) -> str:
    parts = {p.upper() for p in path.parts}
    if "DAI-C-CL" in parts:
        return "clinical"
    if "DAI-C-CO" in parts:
        return "comparison"
    return "unknown"


def is_interactional(text: str) -> bool:
    tags = [tag.upper() for tag, _ in BLOCK.findall(text)]
    has_int = "INT" in tags
    has_participant = any(tag != "INT" for tag in tags)
    return has_int and has_participant and len(TIMESTAMP.findall(text)) < 3


def quantiles(values: list[int]) -> dict[str, float | int | None]:
    if not values:
        return {
            "n": 0, "min": None, "p10": None, "p25": None, "median": None,
            "p75": None, "p90": None, "max": None, "mean": None,
        }
    xs = sorted(values)

    def q(p: float) -> float:
        if len(xs) == 1:
            return float(xs[0])
        pos = (len(xs) - 1) * p
        lo = math.floor(pos)
        hi = math.ceil(pos)
        if lo == hi:
            return float(xs[lo])
        return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)

    return {
        "n": len(xs),
        "min": xs[0],
        "p10": round(q(0.10), 2),
        "p25": round(q(0.25), 2),
        "median": round(statistics.median(xs), 2),
        "p75": round(q(0.75), 2),
        "p90": round(q(0.90), 2),
        "max": xs[-1],
        "mean": round(statistics.fmean(xs), 2),
    }


def parse_transcript(text: str) -> dict:
    blocks = []
    for tag, body in BLOCK.findall(text):
        role = "interviewer" if tag.upper() == "INT" else "participant"
        blocks.append((role, clean_word_count(body)))

    episodes = []
    current = None
    orphan_participant_turns = 0
    orphan_participant_words = 0
    consecutive_interviewer_pairs = 0
    prev_role = None

    for role, words in blocks:
        if role == "interviewer":
            if prev_role == "interviewer":
                consecutive_interviewer_pairs += 1
            if current is not None:
                episodes.append(current)
            current = {
                "interviewer_words": words,
                "participant_words": 0,
                "participant_turns": 0,
            }
        else:
            if current is None:
                orphan_participant_turns += 1
                orphan_participant_words += words
            else:
                current["participant_words"] += words
                current["participant_turns"] += 1
        prev_role = role

    if current is not None:
        episodes.append(current)

    return {
        "blocks": len(blocks),
        "interviewer_turns": sum(1 for role, _ in blocks if role == "interviewer"),
        "participant_turns": sum(1 for role, _ in blocks if role == "participant"),
        "episodes": episodes,
        "orphan_participant_turns": orphan_participant_turns,
        "orphan_participant_words": orphan_participant_words,
        "consecutive_interviewer_pairs": consecutive_interviewer_pairs,
    }


def aggregate(records: list[dict]) -> dict:
    episodes = [ep for rec in records for ep in rec["episodes"]]
    valid = [ep for ep in episodes if ep["participant_turns"] > 0]
    empty = [ep for ep in episodes if ep["participant_turns"] == 0]

    return {
        "transcripts": len(records),
        "interviewer_turns": sum(r["interviewer_turns"] for r in records),
        "participant_turns": sum(r["participant_turns"] for r in records),
        "candidate_episodes": len(episodes),
        "episodes_with_participant_response": len(valid),
        "episodes_without_participant_response": len(empty),
        "orphan_participant_turns": sum(r["orphan_participant_turns"] for r in records),
        "orphan_participant_words": sum(r["orphan_participant_words"] for r in records),
        "consecutive_interviewer_pairs": sum(r["consecutive_interviewer_pairs"] for r in records),
        "participant_words_per_valid_episode": quantiles(
            [ep["participant_words"] for ep in valid]
        ),
        "interviewer_words_per_valid_episode": quantiles(
            [ep["interviewer_words"] for ep in valid]
        ),
        "participant_turns_per_valid_episode": quantiles(
            [ep["participant_turns"] for ep in valid]
        ),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--md-out", required=True)
    args = ap.parse_args()

    root = Path(args.root)
    records_by_cohort = defaultdict(list)
    selected_extensions = Counter()

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".docx", ".rtf"}:
            continue
        if "Full tagged pass" not in str(path):
            continue
        if "Speaker_only_for_analysis" in str(path):
            continue
        text = read_text(path)
        if text is None or not is_interactional(text):
            continue
        cohort = cohort_for(path)
        selected_extensions[path.suffix.lower()] += 1
        records_by_cohort[cohort].append(parse_transcript(text))

    all_records = [r for rs in records_by_cohort.values() for r in rs]
    result = {
        "dataset": "DAIS-C",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "privacy_rule": "No transcript text, file names, or participant IDs emitted.",
        "episode_rule": (
            "One interviewer block starts an episode; all immediately following "
            "participant blocks belong to that episode until the next interviewer block."
        ),
        "selected_source_extensions": dict(sorted(selected_extensions.items())),
        "overall": aggregate(all_records),
        "by_cohort": {
            cohort: aggregate(records)
            for cohort, records in sorted(records_by_cohort.items())
        },
        "quality_gate": {
            "target": (
                "Use episode inventory only for calibration until human raters verify "
                "that block-based boundaries are semantically coherent."
            ),
            "published_sample": {
                "clinical": 15,
                "comparison": 14,
                "total": 29,
            },
            "available_full_interactional_transcripts": {
                cohort: len(records)
                for cohort, records in sorted(records_by_cohort.items())
            },
        },
    }

    jout = Path(args.json_out)
    mout = Path(args.md_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    mout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    overall = result["overall"]
    cohort_rows = []
    for cohort, a in result["by_cohort"].items():
        cohort_rows.append(
            f"| {cohort} | {a['transcripts']} | {a['candidate_episodes']} | "
            f"{a['episodes_with_participant_response']} | "
            f"{a['episodes_without_participant_response']} | "
            f"{a['orphan_participant_turns']} |"
        )

    p = overall["participant_words_per_valid_episode"]
    iw = overall["interviewer_words_per_valid_episode"]
    pt = overall["participant_turns_per_valid_episode"]

    md = f"""# ARIS4C009 Pilot-0 · DAIS-C episode inventory

**Generated:** {result['generated_utc']}

## Privacy rule

No transcript text, participant IDs, or raw file names are emitted.

## Frozen engineering episode rule

> One interviewer block starts an episode. All immediately following participant
> blocks belong to that episode until the next interviewer block.

This is a **parser rule**, not yet a validated phenomenological episode definition.

## Corpus-level result

- full-interaction transcripts selected: {overall['transcripts']}
- interviewer turns: {overall['interviewer_turns']}
- participant turns: {overall['participant_turns']}
- candidate episodes: {overall['candidate_episodes']}
- episodes with participant response: {overall['episodes_with_participant_response']}
- episodes without participant response: {overall['episodes_without_participant_response']}
- orphan participant turns: {overall['orphan_participant_turns']}
- consecutive-interviewer pairs: {overall['consecutive_interviewer_pairs']}

## Cohort structure

| Cohort | Transcripts | Candidate episodes | With response | No response | Orphan participant turns |
|---|---:|---:|---:|---:|---:|
{chr(10).join(cohort_rows)}

## Valid-episode length distributions

### Participant words

- median: {p['median']}
- IQR: {p['p25']}–{p['p75']}
- p10–p90: {p['p10']}–{p['p90']}
- min–max: {p['min']}–{p['max']}

### Interviewer words

- median: {iw['median']}
- IQR: {iw['p25']}–{iw['p75']}
- p10–p90: {iw['p10']}–{iw['p90']}

### Participant turns per episode

- median: {pt['median']}
- IQR: {pt['p25']}–{pt['p75']}
- p10–p90: {pt['p10']}–{pt['p90']}

## Sample-availability note

The DAIS-C publication/data record describes 15 clinical and 14 comparison speakers.
The public archive's full-interaction source layer is inventoried separately here.
A recruited participant without a usable full-interaction source is not silently treated
as an analyzable fidelity episode.

## Human validation gate

Before any semantic/phenomenological fidelity result:

1. draw a calibration-only sample of parsed episodes;
2. have two trained raters judge whether the machine boundary is coherent;
3. record split / merge / reject decisions;
4. revise the parser rule if boundary error is material;
5. freeze the rule before benchmark scoring.

Only after this gate can machine-derived candidate episodes become annotation units.
"""
    mout.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
