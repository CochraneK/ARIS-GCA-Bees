#!/usr/bin/env python3
"""Idempotent branding/link migration for ARIS4C.

Scans maintainable text assets and removes stale repository branding/URLs.
Historical raw command logs are intentionally excluded.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".html", ".tex", ".json", ".py", ".ps1", ".yml", ".yaml"}
EXCLUDED_FILES = {"all_powershell_history.txt"}
EXCLUDED_DIRS = {".git", "__pycache__"}

REPLACEMENTS = (
    ("https://github.com/example/bee-precision-model", "https://github.com/CochraneK/ARIS4C"),
    ("https://github.com/CunyiKang/ARIS-GCA-Bees", "https://github.com/CochraneK/ARIS4C"),
    ("https://github.com/CunyiKang/ARIS4C", "https://github.com/CochraneK/ARIS4C"),
    ("https://github.com/CochraneK/ARIS-GCA-Bees", "https://github.com/CochraneK/ARIS4C"),
    ("https://cunyikang.github.io/ARIS-GCA-Bees/", "https://cunyikang.github.io/ARIS4C/"),
    ("https://cochranek.github.io/ARIS-GCA-Bees/", "https://cochranek.github.io/ARIS4C/"),
    ("CunyiKang/ARIS-GCA-Bees", "CochraneK/ARIS4C"),
    ("CochraneK/ARIS-GCA-Bees", "CochraneK/ARIS4C"),
    ("ARIS-GCA-Bees", "ARIS4C"),
)


def eligible(path: Path) -> bool:
    if path.name in EXCLUDED_FILES:
        return False
    if any(part in EXCLUDED_DIRS for part in path.parts):
        return False
    return path.suffix.lower() in TEXT_SUFFIXES


def migrate(path: Path) -> bool:
    try:
        original = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    updated = original
    for old, new in REPLACEMENTS:
        updated = updated.replace(old, new)
    if updated == original:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    changed: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if path.is_file() and eligible(path) and migrate(path):
            changed.append(str(path.relative_to(ROOT)))

    if changed:
        print("ARIS4C migration updated:")
        for item in changed:
            print(f"  - {item}")
    else:
        print("ARIS4C migration: no stale maintainable references found.")


if __name__ == "__main__":
    main()
