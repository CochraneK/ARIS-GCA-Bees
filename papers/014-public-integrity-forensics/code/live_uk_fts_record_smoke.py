"""Live UK Find a Tender lifecycle record smoke for ARIS4C014.

This smoke starts from recent award releases, selects processes with direct
Companies House supplier identifiers, then fetches complete OCDS record
packages for those OCIDs. It tests whether earlier tender releases add
competition coverage without crossing procurement-process boundaries.

No supplier is ranked or accused.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import time
from urllib.error import HTTPError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from open_integrity_agent import OpenIntegrityAgent
from source_adapters import normalize_ocds_record_package, normalize_ocds_release


RELEASE_BASE = "https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages"
RECORD_BASE = "https://www.find-tender.service.gov.uk/api/1.0/ocdsRecordPackages"


def _get_json(url: str, attempts: int = 4) -> dict:
    for attempt in range(attempts):
        req = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "ARIS4C014-OpenIntegrity/0.1 lifecycle-smoke",
            },
        )
        try:
            with urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code not in {429, 503} or attempt == attempts - 1:
                raise
            retry = exc.headers.get("Retry-After")
            delay = min(float(retry) if retry else 5.0, 30.0)
            time.sleep(delay)
    raise RuntimeError("unreachable")


def recent_award_package(days: int = 7, limit: int = 50) -> tuple[str, dict]:
    now = datetime.now(timezone.utc).replace(microsecond=0)
    start = now - timedelta(days=days)
    params = {
        "updatedFrom": start.strftime("%Y-%m-%dT%H:%M:%S"),
        "updatedTo": now.strftime("%Y-%m-%dT%H:%M:%S"),
        "stages": "award",
        "limit": limit,
    }
    url = RELEASE_BASE + "?" + urlencode(params)
    return url, _get_json(url)


def select_joinable_ocids(package_url: str, package: dict, limit: int) -> list[str]:
    selected: list[str] = []
    for release in package.get("releases") or []:
        imported = normalize_ocds_release(
            release,
            source_name="UK Find a Tender OCDS",
            source_url=package_url,
            jurisdiction="GB",
        )
        if any(
            supplier.startswith("GB-COH:")
            for case in imported.cases
            for supplier in case.contract.supplier_ids
        ):
            ocid = str(release.get("ocid") or "").strip()
            if ocid and ocid not in selected:
                selected.append(ocid)
        if len(selected) >= limit:
            break
    return selected


def run(sample_size: int = 8) -> dict:
    package_url, release_package = recent_award_package()
    ocids = select_joinable_ocids(package_url, release_package, sample_size)
    agent = OpenIntegrityAgent()

    rows = []
    total_cases = 0
    competition_cases = 0
    single_bidder_executed = 0

    for ocid in ocids:
        url = RECORD_BASE + "/" + quote(ocid, safe="")
        package = _get_json(url)
        imported = normalize_ocds_record_package(
            package,
            source_name="UK Find a Tender OCDS record",
            source_url=url,
            jurisdiction="GB",
        )

        process_cases = []
        for case in imported.cases:
            total_cases += 1
            if "procurement_competition" in case.source_coverage:
                competition_cases += 1
            report = agent.run(case)
            single = next(
                f for f in report["findings"]
                if f["detector_id"] == "single_bidder"
            )
            if single["status"] in {"FLAG", "PASS"}:
                single_bidder_executed += 1
            assert report["corruption_inference"] is False
            process_cases.append(
                {
                    "contract_id": case.contract.contract_id,
                    "bid_count": case.contract.bid_count,
                    "procurement_method": case.contract.procurement_method,
                    "source_coverage": sorted(case.source_coverage),
                    "single_bidder_status": single["status"],
                    "gb_coh_suppliers": [
                        x for x in case.contract.supplier_ids
                        if x.startswith("GB-COH:")
                    ],
                }
            )

        rows.append(
            {
                "ocid": ocid,
                "release_count": imported.release_count,
                "case_count": len(imported.cases),
                "warnings": imported.warnings,
                "cases": process_cases,
            }
        )

    return {
        "source": "UK Find a Tender OCDS record packages",
        "selected_ocid_count": len(ocids),
        "total_award_case_count": total_cases,
        "competition_covered_case_count": competition_cases,
        "single_bidder_detector_executed_case_count": single_bidder_executed,
        "competition_coverage_rate": (
            competition_cases / total_cases if total_cases else None
        ),
        "processes": rows,
        "corruption_inference": False,
        "notes": [
            "OCIDs were selected only for Companies House identifier joinability.",
            "Competition data are carried only across releases within the same OCID.",
            "This smoke test measures data coverage, not supplier risk."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="uk_fts_record_smoke.json")
    parser.add_argument("--sample-size", type=int, default=8)
    args = parser.parse_args()
    output = run(args.sample_size)
    Path(args.out).write_text(
        json.dumps(output, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
