"""Live Contracts Finder coverage smoke for ARIS4C014.

Contracts Finder is tested as a complementary UK OCDS source. The smoke measures:
- award normalization;
- direct Companies House supplier identifiers;
- tender.numberOfTenderers availability;
- lifecycle-record enrichment for a few identifier-joinable OCIDs.

It is a coverage test only and produces no supplier risk ranking.
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


SEARCH = "https://www.contractsfinder.service.gov.uk/Published/Notices/OCDS/Search"
RECORD = "https://www.contractsfinder.service.gov.uk/Published/OCDS/Record"
RECORD_COMPAT = "https://www.contractsfinder.service.gov.uk/Published/Notice/records"


def get_json(url: str, attempts: int = 3) -> dict:
    for attempt in range(attempts):
        req = Request(
            url,
            headers={
                "Accept": "application/json",
                "User-Agent": "ARIS4C014-OpenIntegrity/0.1 contracts-finder-smoke",
            },
        )
        try:
            with urlopen(req, timeout=60) as response:
                return json.loads(response.read().decode("utf-8-sig"))
        except HTTPError as exc:
            if attempt == attempts - 1 or exc.code not in {403, 429, 503}:
                raise
            retry = exc.headers.get("Retry-After")
            delay = float(retry) if retry else (10 if exc.code != 403 else 30)
            time.sleep(min(delay, 60))
    raise RuntimeError("unreachable")


def get_record_package(ocid: str) -> tuple[str | None, dict | None, list[str]]:
    errors: list[str] = []
    candidates = [
        RECORD + "/" + quote(ocid, safe=""),
        RECORD_COMPAT + "/" + quote(ocid, safe="") + ".json",
    ]
    for url in candidates:
        try:
            return url, get_json(url), errors
        except HTTPError as exc:
            if exc.code == 404:
                errors.append(f"404:{url}")
                continue
            raise
    return None, None, errors


def search_package(days: int, limit: int) -> tuple[str, dict]:
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=days)
    params = {
        "publishedFrom": start.strftime("%Y-%m-%d"),
        "publishedTo": now.strftime("%Y-%m-%d"),
        "stages": "award",
        "limit": limit,
    }
    url = SEARCH + "?" + urlencode(params)
    return url, get_json(url)


def run(days: int = 30, limit: int = 50, record_sample: int = 5) -> dict:
    search_url, package = search_package(days, limit)
    releases = package.get("releases") or []
    agent = OpenIntegrityAgent()

    release_cases = []
    joinable_ocids = []
    competition_release_cases = 0

    for release in releases:
        imported = normalize_ocds_release(
            release,
            source_name="UK Contracts Finder OCDS",
            source_url=search_url,
            jurisdiction="GB",
        )
        for case in imported.cases:
            if "procurement_competition" in case.source_coverage:
                competition_release_cases += 1
            joinable = [
                x for x in case.contract.supplier_ids if x.startswith("GB-COH:")
            ]
            if joinable:
                ocid = str(release.get("ocid") or "").strip()
                if ocid and ocid not in joinable_ocids:
                    joinable_ocids.append(ocid)
            report = agent.run(case)
            assert report["corruption_inference"] is False
            release_cases.append(
                {
                    "contract_id": case.contract.contract_id,
                    "bid_count": case.contract.bid_count,
                    "gb_coh_suppliers": joinable,
                    "source_coverage": sorted(case.source_coverage),
                }
            )

    lifecycle_rows = []
    lifecycle_cases = 0
    lifecycle_competition_cases = 0
    record_fetch_error_count = 0
    for ocid in joinable_ocids[:record_sample]:
        url, record_package, fetch_errors = get_record_package(ocid)
        if record_package is None or url is None:
            record_fetch_error_count += 1
            lifecycle_rows.append(
                {
                    "ocid": ocid,
                    "record_available": False,
                    "fetch_errors": fetch_errors,
                    "release_count": 0,
                    "award_case_count": 0,
                    "competition_case_count": 0,
                    "warnings": ["record_package_not_available"],
                }
            )
            continue

        imported = normalize_ocds_record_package(
            record_package,
            source_name="UK Contracts Finder OCDS record",
            source_url=url,
            jurisdiction="GB",
        )
        for case in imported.cases:
            lifecycle_cases += 1
            if "procurement_competition" in case.source_coverage:
                lifecycle_competition_cases += 1
        lifecycle_rows.append(
            {
                "ocid": ocid,
                "record_available": True,
                "record_url": url,
                "fetch_errors": fetch_errors,
                "release_count": imported.release_count,
                "award_case_count": len(imported.cases),
                "competition_case_count": sum(
                    "procurement_competition" in x.source_coverage
                    for x in imported.cases
                ),
                "warnings": imported.warnings,
            }
        )

    joinable_case_count = sum(bool(x["gb_coh_suppliers"]) for x in release_cases)
    return {
        "source": "UK Contracts Finder",
        "search_endpoint": SEARCH,
        "record_endpoint": RECORD,
        "record_compat_endpoint": RECORD_COMPAT,
        "release_count": len(releases),
        "award_case_count": len(release_cases),
        "gb_coh_joinable_case_count": joinable_case_count,
        "joinability_rate": (
            joinable_case_count / len(release_cases) if release_cases else None
        ),
        "competition_release_case_count": competition_release_cases,
        "lifecycle_sample_ocid_count": len(lifecycle_rows),
        "lifecycle_award_case_count": lifecycle_cases,
        "lifecycle_competition_case_count": lifecycle_competition_cases,
        "record_fetch_error_count": record_fetch_error_count,
        "lifecycle_rows": lifecycle_rows,
        "sample_release_cases": release_cases[:10],
        "corruption_inference": False,
        "notes": [
            "This is a data coverage test, not a supplier-risk ranking.",
            "Missing bidder counts remain ABSTAIN.",
            "Company-name matching is not used to manufacture GB-COH identifiers."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="contracts_finder_smoke.json")
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--record-sample", type=int, default=5)
    args = parser.parse_args()
    output = run(args.days, args.limit, args.record_sample)
    Path(args.out).write_text(
        json.dumps(output, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
