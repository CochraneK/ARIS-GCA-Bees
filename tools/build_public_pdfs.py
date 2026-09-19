#!/usr/bin/env python3
"""Build bilingual publication PDFs for completed ARIS4C papers."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import markdown
from weasyprint import CSS, HTML

ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "tools" / "pdf_publication.css"

BUILDS = [
    ("001", ROOT / "papers/001-gca-bees/manuscript/MAIN.md", ROOT / "docs/paper/001/en/main.pdf", "en"),
    ("001", ROOT / "papers/001-gca-bees/manuscript/MAIN.zh-CN.md", ROOT / "docs/paper/001/zh/main.pdf", "zh-CN"),
    ("002", ROOT / "papers/002-language-geometry/manuscript/DRAFT.md", ROOT / "docs/paper/002/en/main.pdf", "en"),
    ("002", ROOT / "papers/002-language-geometry/manuscript/DRAFT.zh-CN.md", ROOT / "docs/paper/002/zh/main.pdf", "zh-CN"),
]

EXTENSIONS = [
    "tables",
    "fenced_code",
    "sane_lists",
    "attr_list",
]

def first_heading(md: str) -> str:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "ARIS4C paper"

def build_one(source: Path, output: Path, lang: str) -> None:
    md = source.read_text(encoding="utf-8")
    title = first_heading(md)
    body = markdown.markdown(md, extensions=EXTENSIONS, output_format="html5")
    doc = f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
</head>
<body>{body}</body>
</html>"""
    output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=doc, base_url=str(source.parent)).write_pdf(
        str(output),
        stylesheets=[CSS(filename=str(CSS_PATH))],
        presentational_hints=True,
    )
    if not output.exists() or output.stat().st_size < 20_000:
        raise RuntimeError(f"PDF build looks incomplete: {output}")

def main() -> int:
    missing = [str(src) for _, src, _, _ in BUILDS if not src.exists()]
    if missing:
        print("Missing sources:", *missing, sep="\n- ", file=sys.stderr)
        return 2
    for pid, src, out, lang in BUILDS:
        build_one(src, out, lang)
        print(f"built {pid} {lang}: {out.relative_to(ROOT)} ({out.stat().st_size:,} bytes)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
