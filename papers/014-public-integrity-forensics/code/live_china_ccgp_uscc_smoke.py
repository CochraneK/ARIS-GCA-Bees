"""Live regression smoke for CCGP supplier unified social credit codes.

Uses one public CCGP award page known to expose supplier USCC values. The
artifact is aggregate-only: no supplier addresses, telephone numbers or contact
persons are emitted.
"""

from __future__ import annotations

from datetime import datetime
from hashlib import sha256
import json
from pathlib import Path

from china_ccgp import fetch_text
from china_ccgp_detail import parse_ccgp_award_detail


SOURCE_URL = (
    "https://www.ccgp.gov.cn/cggg/dfgg/zbgg/202609/"
    "t20260914_27325491.htm"
)


def main() -> None:
    html = fetch_text(SOURCE_URL)
    retrieved_at = datetime.now().astimezone().isoformat()
    notice = parse_ccgp_award_detail(
        html,
        source_url=SOURCE_URL,
        retrieved_at=retrieved_at,
    )

    final_lots = [x for x in notice.lots if x.result_status == "awarded"]
    with_uscc = [x for x in final_lots if x.supplier_uscc]
    payload = {
        "source_url": SOURCE_URL,
        "retrieved_at": retrieved_at,
        "html_sha256": sha256(html.encode("utf-8")).hexdigest(),
        "project_id": notice.project_id,
        "final_award_lots": len(final_lots),
        "final_award_lots_with_uscc": len(with_uscc),
        "uscc_coverage": len(with_uscc) / len(final_lots) if final_lots else 0.0,
        "warnings": list(notice.warnings),
        "corruption_inference": False,
        "privacy_note": (
            "Aggregate regression artifact only; supplier names, addresses, "
            "phone numbers and contact persons are not emitted."
        ),
    }

    out = Path("ccgp_uscc_smoke.json")
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))

    if not final_lots:
        raise SystemExit("No final award lots parsed from known USCC page")
    if not with_uscc:
        raise SystemExit("No supplier USCC parsed from known USCC page")


if __name__ == "__main__":
    main()
