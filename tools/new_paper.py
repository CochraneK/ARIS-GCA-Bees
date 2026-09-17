#!/usr/bin/env python3
"""Create a numbered ARIS paper workspace and metadata manifest."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    return value or "paper"


def next_id() -> str:
    ids = []
    if PAPERS.exists():
        for path in PAPERS.iterdir():
            if path.is_dir() and re.match(r"^\d{3}-", path.name):
                ids.append(int(path.name[:3]))
    return f"{max(ids, default=0) + 1:03d}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("title")
    parser.add_argument("--slug")
    parser.add_argument("--year", type=int, default=2026)
    parser.add_argument("--aris-version", default="v0.4.26")
    args = parser.parse_args()

    paper_id = next_id()
    slug = slugify(args.slug or args.title)
    paper_dir = PAPERS / f"{paper_id}-{slug}"
    if paper_dir.exists():
        raise SystemExit(f"Already exists: {paper_dir}")

    for rel in ("code", "data", "figures", "manuscript", "process"):
        target = paper_dir / rel
        target.mkdir(parents=True, exist_ok=True)
        (target / ".gitkeep").write_text("", encoding="utf-8")

    manifest = {
        "id": paper_id,
        "slug": slug,
        "title": args.title,
        "short_title": args.title,
        "year": args.year,
        "status": "idea",
        "domain": "",
        "summary": "",
        "authors": ["Cunyi Kang"],
        "aris": {
            "provenance": "ARIS",
            "version": args.aris_version,
            "commit": "RECORD-EXACT-COMMIT-BEFORE-RUN"
        },
        "links": {
            "paper_en": "",
            "paper_zh": "",
            "pipeline": "",
            "source": ""
        },
        "tags": []
    }
    (paper_dir / "paper.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (paper_dir / "README.md").write_text(
        f"# {args.title}\n\nStatus: idea\n\nARIS: {args.aris_version}\n",
        encoding="utf-8",
    )
    print(paper_dir.relative_to(ROOT))


if __name__ == "__main__":
    main()
