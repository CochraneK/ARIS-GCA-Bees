#!/usr/bin/env python3
"""Regression audit for ARIS4C bilingual repository README surfaces."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
REQUIRED_ASSETS = {
    "hero.svg",
    "portfolio-status.svg",
    "portfolio-maturity.svg",
    "delivery-readiness.svg",
    "architecture.svg",
    "paper-structure.svg",
    "paper-lifecycle.svg",
    "handoff-package.svg",
}


def fail(msg: str, errors: list[str]) -> None:
    errors.append(msg)


def relative_targets(text: str) -> list[str]:
    md = re.findall(r"\]\((?!https?://|#)([^)]+)\)", text)
    html = re.findall(r'(?:src|href)="(\./[^"]+)"', text)
    return md + html


def audit_readme(path: Path, lang: str, project_ids: list[str], errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    label = path.name

    if "\\`" in text:
        fail(f"{label}: escaped backticks remain", errors)
    if re.search(r"near[- ]?final", text, re.I):
        fail(f"{label}: obsolete near-final terminology found", errors)
    if re.search(r"Cunyi Kang", text, re.I):
        fail(f"{label}: obsolete author name found", errors)

    expected_asset_prefix = f"./docs/assets/readme/{lang}/"
    other = "en" if lang == "zh" else "zh"
    if f"./docs/assets/readme/{other}/" in text:
        fail(f"{label}: cross-language README image reference found", errors)

    refs = set(re.findall(rf"docs/assets/readme/{lang}/([^\"\)\s]+)", text))
    if refs != REQUIRED_ASSETS:
        fail(f"{label}: README asset set mismatch: {sorted(refs)}", errors)

    table_ids = re.findall(r"^\| \*\*([0-9]{3})\*\* \|", text, re.M)
    if table_ids != project_ids:
        fail(f"{label}: project table IDs mismatch: {table_ids}", errors)

    handoff_links = re.findall(r"handoff/AGENT_HANDOFF\.md", text)
    if len(handoff_links) != len(project_ids):
        fail(f"{label}: expected {len(project_ids)} handoff links, got {len(handoff_links)}", errors)

    for raw in relative_targets(text):
        target = raw.split("#", 1)[0]
        if target.startswith("./"):
            target = target[2:]
        if not target:
            continue
        candidate = ROOT / target
        if not candidate.exists():
            fail(f"{label}: broken relative target {raw}", errors)

    if lang == "zh":
        if 'href="./README.en.md"' not in text or 'href="./README.md"' not in text:
            fail(f"{label}: Chinese-default language switch is incomplete", errors)
        if "是一个通过" not in text:
            fail(f"{label}: default README does not look Chinese", errors)
    else:
        if 'href="./README.md"' not in text or 'href="./README.en.md"' not in text:
            fail(f"{label}: English language switch is incomplete", errors)
        if "is a living research portfolio" not in text:
            fail(f"{label}: English README does not look English", errors)


def main() -> int:
    manifests = sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json"))
    project_ids = [p.parent.name[:3] for p in manifests]
    errors: list[str] = []

    zh = ROOT / "README.md"
    en = ROOT / "README.en.md"
    legacy = ROOT / "README.zh-CN.md"

    for p in (zh, en, legacy):
        if not p.is_file():
            fail(f"missing README surface: {p.name}", errors)

    for lang in ("zh", "en"):
        directory = ROOT / "docs" / "assets" / "readme" / lang
        names = {p.name for p in directory.glob("*.svg")} if directory.is_dir() else set()
        if names != REQUIRED_ASSETS:
            fail(f"{lang} asset directory mismatch: {sorted(names)}", errors)

    if zh.is_file():
        audit_readme(zh, "zh", project_ids, errors)
    if en.is_file():
        audit_readme(en, "en", project_ids, errors)
    if zh.is_file() and legacy.is_file() and zh.read_text(encoding="utf-8") != legacy.read_text(encoding="utf-8"):
        fail("README.zh-CN.md is no longer an exact compatibility mirror of README.md", errors)

    if errors:
        print("README audit FAIL", file=sys.stderr)
        for e in errors:
            print(f"- {e}", file=sys.stderr)
        return 1

    print(f"README audit PASS: {len(project_ids)} papers, {len(REQUIRED_ASSETS)} assets × 2 languages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
