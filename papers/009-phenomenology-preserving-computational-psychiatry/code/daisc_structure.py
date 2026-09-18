#!/usr/bin/env python3
"""Classify DAIS-C assets without emitting interview content or participant IDs."""

from __future__ import annotations

import argparse, html, json, re, zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

TEXT_EXTENSIONS = {".txt", ".rtf", ".docx"}
PARTICIPANT_ID = re.compile(r"[0-9]{2}[A-Z]{2}[0-9]{2}")
PARTICIPANT_BLOCK = re.compile(r"<([0-9]{2}[A-Z]{2}[0-9]{2})>(.*?)</\1>", re.DOTALL)
INT_BLOCK = re.compile(r"<INT>(.*?)</INT>", re.DOTALL | re.IGNORECASE)
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
        paragraphs = []
        for paragraph in root.findall(".//w:p", ns):
            pieces = []
            for node in paragraph.iter():
                if node.tag.endswith("}t") and node.text:
                    pieces.append(node.text)
                elif node.tag.endswith("}tab"):
                    pieces.append("\t")
                elif node.tag.endswith("}br"):
                    pieces.append("\n")
            if pieces:
                paragraphs.append("".join(pieces))
        return "\n".join(paragraphs)
    except Exception:
        return None


def safe_read(path: Path) -> str | None:
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


def clean_words(text: str) -> int:
    text = XML_TAG.sub(" ", text)
    text = RTF_CONTROL.sub(" ", text)
    text = text.replace("{", " ").replace("}", " ")
    return len(WORD.findall(text))


def classify(text: str):
    pblocks = PARTICIPANT_BLOCK.findall(text)
    iblocks = INT_BLOCK.findall(text)
    timestamps = len(TIMESTAMP.findall(text))
    pwords = sum(clean_words(block) for _, block in pblocks)
    iwords = sum(clean_words(block) for block in iblocks)
    ids = {pid for pid, _ in pblocks}
    if timestamps >= 3 and pblocks:
        kind = "timestamped"
    elif pblocks and iblocks and pwords >= 50:
        kind = "interactional"
    elif pblocks and not iblocks and pwords >= 50:
        kind = "speaker_only_xml"
    elif pblocks:
        kind = "participant_tagged_other"
    else:
        kind = "non_transcript_text"
    return kind, pwords, iwords, timestamps, ids


def sanitize(value: str) -> str:
    value = PARTICIPANT_ID.sub("<PID>", value)
    return re.sub(r"\d{4,}", "<N>", value)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--md-out", required=True)
    args = ap.parse_args()
    root = Path(args.root)

    counts = Counter()
    ext_by_kind = defaultdict(Counter)
    pwords = Counter()
    iwords = Counter()
    timestamps = Counter()
    ids_by_kind = defaultdict(set)
    readable = Counter()
    patterns = Counter()

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = safe_read(path)
        if text is None:
            continue
        readable[path.suffix.lower()] += 1
        kind, pw, iw, ts, ids = classify(text)
        counts[kind] += 1
        ext_by_kind[kind][path.suffix.lower()] += 1
        pwords[kind] += pw
        iwords[kind] += iw
        timestamps[kind] += ts
        ids_by_kind[kind].update(ids)
        rel = "/".join(sanitize(x) for x in path.relative_to(root).parts)
        patterns[f"{kind}: {rel}"] += 1

    result = {
        "dataset": "DAIS-C",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "privacy_rule": "No transcript text or participant IDs emitted.",
        "readable_files_by_extension": dict(sorted(readable.items())),
        "classification_counts": dict(sorted(counts.items())),
        "extensions_by_class": {k: dict(sorted(v.items())) for k, v in sorted(ext_by_kind.items())},
        "participant_word_counts_by_class": dict(sorted(pwords.items())),
        "interviewer_word_counts_by_class": dict(sorted(iwords.items())),
        "timestamp_markers_by_class": dict(sorted(timestamps.items())),
        "unique_participant_id_counts_by_class": {k: len(v) for k, v in sorted(ids_by_kind.items())},
        "sanitized_path_pattern_counts": dict(sorted(patterns.items())),
        "published_reference": {
            "paper_total_tokens": 97357,
            "paper_clinical_tokens": 58444,
            "paper_comparison_tokens": 33025,
            "paper_audio_minutes": 1284.8,
        },
    }

    jout, mout = Path(args.json_out), Path(args.md_out)
    jout.parent.mkdir(parents=True, exist_ok=True)
    mout.parent.mkdir(parents=True, exist_ok=True)
    jout.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    rows = [
        f"| {k} | {counts[k]} | {len(ids_by_kind[k])} | {pwords[k]:,} | {iwords[k]:,} |"
        for k in sorted(counts)
    ]
    pattern_rows = [f"- `{p}` × {n}" for p, n in sorted(patterns.items())]
    ext_rows = [f"- `{e}`: {n}" for e, n in sorted(readable.items())]

    md = f"""# ARIS4C009 Pilot-0 · DAIS-C structural classification

**Generated:** {result['generated_utc']}

## Privacy rule
No transcript text or participant IDs are emitted. TXT/RTF/DOCX parsing occurs only
inside the transient GitHub Actions runner.

## Readable formats
{chr(10).join(ext_rows) or '- none'}

## Structural classes
| Class | Files | Unique pseudonymous speaker IDs | Participant words | Interviewer words |
|---|---:|---:|---:|---:|
{chr(10).join(rows)}

## Sanitized archive path patterns
Speaker identifiers and long numeric strings are masked.
{chr(10).join(pattern_rows) or '- none'}

## Published validation reference
The DAIS-C paper reports approximately 97,357 total corpus tokens
(58,444 clinical; 33,025 comparison) and 1,284.8 audio minutes.
These are validation references rather than exact tokenizer targets.

## Canonical-source gate
A source class is acceptable only if it contains interviewer + participant speech,
excludes timestamp-only versions, has plausible corpus scale, and does not duplicate
the same interview through multiple formats.

If no full-interaction class passes, Pilot-0 must either use speaker-only XML with an
explicit context limitation or switch corpus.

## Next gate
Freeze an episode parser only after the canonical source class is identified.
"""
    mout.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
