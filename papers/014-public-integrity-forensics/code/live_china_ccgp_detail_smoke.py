"""Bounded live CCGP detail normalization smoke."""

from datetime import datetime
from pathlib import Path

from china_ccgp import discover_live, fetch_text
from china_ccgp_detail import dump_detail_report, parse_ccgp_award_detail, safe_structural_debug_lines


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
    debug_printed = False
    for url in urls:
        try:
            html = fetch_text(url)
            notice = parse_ccgp_award_detail(
                html,
                source_url=url,
                retrieved_at=retrieved_at,
            )
            notices.append(notice)
            if not notice.lots and not debug_printed:
                print("SAFE_STRUCTURE_DEBUG")
                for line in safe_structural_debug_lines(html):
                    print(line)
                print("END_SAFE_STRUCTURE_DEBUG")
                debug_printed = True
        except Exception as exc:
            print(f"detail_fetch_failed:{url}:{type(exc).__name__}")

    out = Path("ccgp_detail_pilot0.json")
    out.write_text(dump_detail_report(notices), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
