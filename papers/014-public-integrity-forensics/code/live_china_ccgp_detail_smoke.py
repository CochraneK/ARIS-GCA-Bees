"""Bounded live CCGP detail normalization smoke."""

from datetime import datetime
from pathlib import Path

from china_ccgp import discover_live
from china_ccgp_detail import dump_detail_report, fetch_and_parse_detail


def main() -> None:
    retrieved_at = datetime.now().astimezone().isoformat()
    discovery = discover_live(per_page_limit=8)
    urls = []
    for result in discovery:
        for lead in result.leads:
            if lead.url not in urls:
                urls.append(lead.url)
    urls = urls[:12]

    notices = []
    for url in urls:
        try:
            notices.append(fetch_and_parse_detail(url, retrieved_at=retrieved_at))
        except Exception as exc:
            print(f"detail_fetch_failed:{url}:{type(exc).__name__}")

    out = Path("ccgp_detail_pilot0.json")
    out.write_text(dump_detail_report(notices), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
