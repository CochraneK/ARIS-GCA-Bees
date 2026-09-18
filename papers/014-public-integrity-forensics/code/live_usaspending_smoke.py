"""Live USAspending smoke test for ARIS4C014.

This is not a detector benchmark. It only verifies that a current public API
response can be normalized by OpenIntegrity without turning missing source
coverage into negative evidence or producing an automated corruption claim.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.request import Request, urlopen

from open_integrity_agent import OpenIntegrityAgent
from source_adapters import normalize_usaspending_award


API = "https://api.usaspending.gov/api/v2/search/spending_by_award/"


def fetch_rows() -> dict:
    payload = {
        "filters": {
            "award_type_codes": ["A", "B", "C", "D"],
            "time_period": [
                {"start_date": "2025-01-01", "end_date": "2025-12-31"}
            ],
        },
        "fields": [
            "Award ID",
            "Recipient Name",
            "Recipient UEI",
            "recipient_id",
            "Awarding Agency",
            "Awarding Agency Code",
            "Award Amount",
            "Base Obligation Date",
            "Last Modified Date",
            "Contract Award Type",
        ],
        "limit": 3,
        "page": 1,
        "sort": "Award Amount",
        "order": "desc",
        "subawards": False,
    }
    body = json.dumps(payload).encode("utf-8")
    req = Request(
        API,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "ARIS4C014-OpenIntegrity/0.1 public-data-smoke",
        },
        method="POST",
    )
    with urlopen(req, timeout=45) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize_response(data: dict) -> dict:
    rows = data.get("results") or []
    if not rows:
        raise RuntimeError("USAspending returned no award rows for the smoke query")

    normalized = []
    agent = OpenIntegrityAgent()
    for row in rows:
        imported = normalize_usaspending_award(row)
        report = agent.run(imported.case)
        assert report["corruption_inference"] is False
        assert all(f["corruption_inference"] is False for f in report["findings"])
        normalized.append(
            {
                "contract_id": imported.case.contract.contract_id,
                "authority_id": imported.case.contract.authority_id,
                "supplier_ids": list(imported.case.contract.supplier_ids),
                "award_date": (
                    imported.case.contract.award_date.isoformat()
                    if imported.case.contract.award_date
                    else None
                ),
                "award_value": imported.case.contract.award_value,
                "source_coverage": sorted(imported.case.source_coverage),
                "adapter_warnings": imported.warnings,
                "review_priority": report["review_priority"],
                "finding_statuses": {
                    f["detector_id"]: f["status"] for f in report["findings"]
                },
                "corruption_inference": report["corruption_inference"],
            }
        )

    return {
        "source": "USAspending",
        "endpoint": API,
        "query_period": ["2025-01-01", "2025-12-31"],
        "row_count": len(rows),
        "messages": data.get("messages") or [],
        "normalized": normalized,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="usaspending_smoke.json")
    args = parser.parse_args()

    data = fetch_rows()
    output = normalize_response(data)
    path = Path(args.out)
    path.write_text(json.dumps(output, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
