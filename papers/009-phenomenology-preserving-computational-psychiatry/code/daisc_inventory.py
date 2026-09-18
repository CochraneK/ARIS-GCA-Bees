#!/usr/bin/env python3
"""Create a non-content inventory for a locally extracted DAIS-C archive.

The script intentionally does NOT emit transcript text. It records only structural
and aggregate properties needed to decide whether the corpus can support ARIS4C009
Pilot-0.

Usage:
    python daisc_inventory.py --root /path/to/extracted \
        --archive /path/to/DAIS-C-Annotated-Upload.7z \
        --json-out data/pilot0_daisc_inventory.json \
        --md-out process/PILOT0_DAISC_INVENTORY.md
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

TEXT_EXTENSIONS = {
    ".txt", ".xml", ".csv", ".tsv", ".md", ".text", ".rtf", ".html", ".htm"
}
TRANSCRIPT_HINTS = ("trans", "interview", "annotat", "corpus", "clinical")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_read(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="latin-1")
        except Exception:
            return None
    except Exception:
        return None


def word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text, flags=re.UNICODE))


def xml_like_tag_count(text: str) -> int:
    return len(re.findall(r"</?[A-Za-z][^>]{0,100}>", text))


def line_count(text: str) -> int:
    return text.count("\n") + (1 if text else 0)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--archive")
    ap.add_argument("--json-out", required=True)
    ap.add_argument("--md-out", required=True)
    args = ap.parse_args()

    root = Path(args.root)
    files = [p for p in root.rglob("*") if p.is_file()]
    ext_counts = Counter((p.suffix.lower() or "<none>") for p in files)

    text_files = []
    aggregate_words = 0
    aggregate_lines = 0
    aggregate_xml_tags = 0
    readable_text_files = 0
    likely_transcript_files = 0
    size_bins = Counter()

    for p in files:
        size = p.stat().st_size
        if size < 10_000:
            size_bins["<10KB"] += 1
        elif size < 100_000:
            size_bins["10-100KB"] += 1
        elif size < 1_000_000:
            size_bins["100KB-1MB"] += 1
        else:
            size_bins[">=1MB"] += 1

        if p.suffix.lower() not in TEXT_EXTENSIONS:
            continue

        text = safe_read(p)
        if text is None:
            continue

        readable_text_files += 1
        wc = word_count(text)
        lc = line_count(text)
        tags = xml_like_tag_count(text)
        aggregate_words += wc
        aggregate_lines += lc
        aggregate_xml_tags += tags

        name_hint = any(h in p.name.lower() for h in TRANSCRIPT_HINTS)
        content_size_hint = wc >= 200
        if name_hint or content_size_hint:
            likely_transcript_files += 1

        text_files.append({
            "extension": p.suffix.lower() or "<none>",
            "bytes": size,
            "words": wc,
            "lines": lc,
            "xml_like_tags": tags,
            "likely_transcript": bool(name_hint or content_size_hint),
        })

    archive_path = Path(args.archive) if args.archive else None
    archive_hash = (
        sha256(archive_path)
        if archive_path and archive_path.exists()
        else None
    )

    result = {
        "dataset": "DAIS-C",
        "source_record": "UK Data Service ReShare 855021",
        "doi": "10.5255/UKDA-SN-855021",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "privacy_rule": "No transcript content emitted by this inventory.",
        "archive_sha256": archive_hash,
        "file_count": len(files),
        "extension_counts": dict(sorted(ext_counts.items())),
        "size_bins": dict(sorted(size_bins.items())),
        "readable_text_files": readable_text_files,
        "likely_transcript_files": likely_transcript_files,
        "aggregate_text_words": aggregate_words,
        "aggregate_text_lines": aggregate_lines,
        "aggregate_xml_like_tags": aggregate_xml_tags,
        "text_file_structural_records": text_files,
    }

    json_out = Path(args.json_out)
    md_out = Path(args.md_out)
    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)

    json_out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    ext_md = "\n".join(
        f"- `{ext}`: {count}" for ext, count in result["extension_counts"].items()
    )
    bin_md = "\n".join(
        f"- {bucket}: {count}" for bucket, count in result["size_bins"].items()
    )

    md = f"""# ARIS4C009 Pilot-0 · DAIS-C inventory

**Generated:** {result['generated_utc']}  
**Source:** UK Data Service ReShare 855021  
**DOI:** 10.5255/UKDA-SN-855021

## Privacy rule

No transcript content is emitted by the inventory job. Raw corpus files are downloaded
only into the transient GitHub Actions runner workspace and are not committed.

## Archive

- SHA-256: `{archive_hash or 'not recorded'}`
- extracted file count: {result['file_count']}
- readable text-like files: {readable_text_files}
- likely transcript-like files: {likely_transcript_files}

## Aggregate structure

- approximate words across readable text-like files: {aggregate_words:,}
- text lines: {aggregate_lines:,}
- XML-like tags: {aggregate_xml_tags:,}

### Extensions

{ext_md or '- none'}

### File-size bins

{bin_md or '- none'}

## Interpretation

This inventory is an engineering artifact only. It does not identify symptoms,
phenomenological states, diagnoses, or participant-level outcomes.

The next gate is to inspect corpus documentation and define a frozen transcript/episode
parser without publishing raw interview text.
"""
    md_out.write_text(md, encoding="utf-8")


if __name__ == "__main__":
    main()
