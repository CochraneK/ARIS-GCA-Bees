#!/usr/bin/env python3
"""Audit continuity readiness for every ARIS4C paper."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ROOT / "papers"
REQUIRED = [
    "README.md",
    "STATUS.md",
    "TODO.md",
    "DECISIONS.md",
    "CONTEXT.md",
    "CHATLOG.md",
    "AGENT_HANDOFF.md",
    "SESSION_LOG.md",
]


def main() -> int:
    rows = []
    failures = []
    for manifest in sorted(PAPERS.glob("[0-9][0-9][0-9]-*/paper.json")):
        pid = manifest.parent.name[:3]
        handoff = manifest.parent / "handoff"
        missing = [name for name in REQUIRED if not (handoff / name).is_file()]
        empty = [name for name in REQUIRED if (handoff / name).is_file() and not (handoff / name).read_text(encoding="utf-8").strip()]
        chat_ok = (handoff / "CHATLOG.md").is_file() and "## " in (handoff / "CHATLOG.md").read_text(encoding="utf-8")
        handoff_ok = (handoff / "AGENT_HANDOFF.md").is_file() and "Immediate next action" in (handoff / "AGENT_HANDOFF.md").read_text(encoding="utf-8")
        ok = not missing and not empty and chat_ok and handoff_ok
        rows.append((pid, "PASS" if ok else "FAIL", missing, empty, chat_ok, handoff_ok))
        if not ok:
            failures.append(pid)

    print("| ID | continuity | missing | empty | chat record | takeover brief |")
    print("|---|---|---|---|---|---|")
    for pid, status, missing, empty, chat_ok, handoff_ok in rows:
        print(f"| {pid} | {status} | {', '.join(missing) or '—'} | {', '.join(empty) or '—'} | {'Y' if chat_ok else 'N'} | {'Y' if handoff_ok else 'N'} |")

    if failures:
        print("\nContinuity-incomplete projects: " + ", ".join(failures), file=sys.stderr)
        return 1
    print(f"\nContinuity audit PASS: {len(rows)} / {len(rows)} projects")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
