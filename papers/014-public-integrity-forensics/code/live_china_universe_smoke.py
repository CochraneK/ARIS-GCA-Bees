from pathlib import Path

from china_universe import dump_universe_report, fetch_live_universes


def main() -> None:
    snapshots = fetch_live_universes()
    out = Path("china_universe_pilot0.json")
    out.write_text(dump_universe_report(snapshots), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
