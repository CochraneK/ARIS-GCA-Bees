#!/usr/bin/env python3
"""DAIS-C structural segmentation sensitivity for ARIS4C009 Pilot-0.

Builds multi-turn windows at several participant-word targets and emits aggregate
statistics only. No transcript text, file names, or participant IDs are written.
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
TARGETS = (20, 40, 80)


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


def wc(text: str) -> int:
    text = XML_TAG.sub(" ", text)
    text = RTF_CONTROL.sub(" ", text)
    text = text.replace("{", " ").replace("}", " ")
    return len(WORD.findall(text))


def cohort(path: Path) -> str:
    parts = {x.upper() for x in path.parts}
    if "DAI-C-CL" in parts:
        return "clinical"
    if "DAI-C-CO" in parts:
        return "comparison"
    return "unknown"


def parse_microepisodes(text: str) -> list[dict]:
    blocks = [
        ("interviewer" if tag.upper() == "INT" else "participant", wc(body))
        for tag, body in BLOCK.findall(text)
    ]
    episodes = []
    current = None
    for role, words in blocks:
        if role == "interviewer":
            if current is not None:
                episodes.append(current)
            current = {
                "interviewer_words": words,
                "participant_words": 0,
                "participant_turns": 0,
            }
        elif current is not None:
            current["participant_words"] += words
            current["participant_turns"] += 1
    if current is not None:
        episodes.append(current)
    return episodes


def accumulate(microepisodes: list[dict], target: int) -> list[dict]:
    windows = []
    current = None
    for ep in microepisodes:
        if current is None:
            current = {
                "participant_words": 0,
                "interviewer_words": 0,
                "participant_turns": 0,
                "microepisodes": 0,
            }
        current["participant_words"] += ep["participant_words"]
        current["interviewer_words"] += ep["interviewer_words"]
        current["participant_turns"] += ep["participant_turns"]
        current["microepisodes"] += 1

        if current["participant_words"] >= target:
            windows.append(current)
            current = None

    if current is not None:
        windows.append(current)
    return windows


def dist(values: list[int]) -> dict:
    if not values:
        return {"n": 0}
    xs = sorted(values)

    def q(p: float) -> float:
        if len(xs) == 1:
            return float(xs[0])
        pos = (len(xs) - 1) * p
        lo, hi = math.floor(pos), math.ceil(pos)
        if lo == hi:
            return float(xs[lo])
        return xs[lo] + (xs[hi] - xs[lo]) * (pos - lo)

    return {
        "n": len(xs),
        "min": xs[0],
        "p10": round(q(.10), 2),
        "p25": round(q(.25), 2),
        "median": round(statistics.median(xs), 2),
        "p75": round(q(.75), 2),
        "p90": round(q(.90), 2),
        "max": xs[-1],
        "mean": round(statistics.fmean(xs), 2),
    }


def summarize(windows: list[dict], target: int) -> dict:
    pwords = [w["participant_words"] for w in windows]
    return {
        "target_participant_words": target,
        "windows": len(windows),
        "participant_words": dist(pwords),
        "interviewer_words": dist([w["interviewer_words"] for w in windows]),
        "microepisodes_per_window": dist([w["microepisodes"] for w in windows]),
        "participant_turns_per_window": dist([w["participant_turns"] for w in windows]),
        "below_target_windows": sum(x < target for x in pwords),
        "zero_participant_word_windows": sum(x == 0 for x in pwords),
        "over_250_participant_word_windows": sum(x > 250 for x in pwords),
        "over_500_participant_word_windows": sum(x > 500 for x in pwords),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--md-out", required=True)
    args = ap.parse_args()

    root = Path(args.root)
    transcripts = defaultdict(list)

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".docx", ".rtf"}:
            continue
        if "Full tagged pass" not in str(path) or "Speaker_only_for_analysis" in str(path):
            continue
        text = read_text(path)
        if text is None:
            continue
        tags = [tag.upper() for tag, _ in BLOCK.findall(text)]
        if "INT" not in tags or not any(t != "INT" for t in tags):
            continue
        if len(TIMESTAMP.findall(text)) >= 3:
            continue
        transcripts[cohort(path)].append(parse_microepisodes(text))

    result = {
        "dataset": "DAIS-C",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "privacy_rule": "No transcript text, file names, or participant IDs emitted.",
        "rule": (
            "Greedily accumulate adjacent interviewer-response microepisodes until "
            "participant-word target is reached; never split inside a source turn."
        ),
        "targets": {},
    }

    for target in TARGETS:
        by_cohort = {}
        all_windows = []
        for c, transcript_eps in sorted(transcripts.items()):
            cohort_windows = []
            for eps in transcript_eps:
                cohort_windows.extend(accumulate(eps, target))
            by_cohort[c] = summarize(cohort_windows, target)
            all_windows.extend(cohort_windows)
        result["targets"][str(target)] = {
            "overall": summarize(all_windows, target),
            "by_cohort": by_cohort,
        }

    jout, mout = Path(args.json_out), Path(args.md_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    mout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    rows = []
    for target in TARGETS:
        s = result["targets"][str(target)]["overall"]
        pw = s["participant_words"]
        mw = s["microepisodes_per_window"]
        rows.append(
            f"| {target} | {s['windows']} | {pw['median']} | "
            f"{pw['p25']}–{pw['p75']} | {mw['median']} | "
            f"{s['below_target_windows']} | {s['over_250_participant_word_windows']} |"
        )

    md = f"""# ARIS4C009 Pilot-0 · Segmentation sensitivity

**Generated:** {result['generated_utc']}

## Privacy rule
No transcript text, file names, or participant IDs are emitted.

## Structural strategy
Adjacent interviewer-response microepisodes are greedily accumulated until a target
number of participant words is reached. Source turns are never split.

This does **not** claim that word count defines phenomenological episodes. It creates
candidate windows for human calibration.

| Target participant words | Windows | Median participant words | IQR | Median microepisodes/window | Below target | >250 words |
|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(rows)}

## Interpretation rule

The preferred engineering target should:

- eliminate most trivial one-word/yes-no units;
- keep most windows short enough for independent human reconstruction;
- avoid requiring many unrelated question-answer pairs per window;
- preserve enough windows for calibration and later benchmarking.

No target becomes canonical from these statistics alone.

## Next gate
Select one or at most two candidate targets for a blinded human boundary-calibration
sample. Human split/merge/reject judgments determine whether the structural rule is
acceptable.
"""
    mout.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
