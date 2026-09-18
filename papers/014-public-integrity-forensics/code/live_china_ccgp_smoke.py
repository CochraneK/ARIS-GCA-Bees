"""Run a bounded live CCGP source-feasibility smoke and save aggregate output."""

from __future__ import annotations

from pathlib import Path

from china_ccgp import discover_live, dumps_live_report


def main() -> None:
    results = discover_live(per_page_limit=50)
    out = Path("ccgp_pilot0.json")
    out.write_text(dumps_live_report(results), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
