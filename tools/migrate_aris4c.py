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

LEGACY_NAME = "ARIS" + "-GCA-Bees"
CURRENT_NAME = "ARIS4C"
CURRENT_REPO = "https://github.com/CochraneK/" + CURRENT_NAME

REPLACEMENTS = (
    ("https://github.com/example/bee-precision-model", CURRENT_REPO),
    ("https://github.com/CunyiKang/" + LEGACY_NAME, CURRENT_REPO),
    ("https://github.com/CunyiKang/" + CURRENT_NAME, CURRENT_REPO),
    ("https://github.com/CochraneK/" + LEGACY_NAME, CURRENT_REPO),
    ("https://cunyikang.github.io/" + LEGACY_NAME + "/", "https://cunyikang.github.io/" + CURRENT_NAME + "/"),
    ("https://cochranek.github.io/" + LEGACY_NAME + "/", "https://cochranek.github.io/" + CURRENT_NAME + "/"),
    ("CunyiKang/" + LEGACY_NAME, "CochraneK/" + CURRENT_NAME),
    ("CochraneK/" + LEGACY_NAME, "CochraneK/" + CURRENT_NAME),
    (LEGACY_NAME, CURRENT_NAME),
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
