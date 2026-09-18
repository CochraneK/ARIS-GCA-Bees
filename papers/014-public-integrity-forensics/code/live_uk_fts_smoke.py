"""Live UK Find a Tender OCDS smoke test for ARIS4C014.

The smoke test:
1. fetches a bounded recent award-stage release window from the official public
   Find a Tender OCDS release-package endpoint;
2. creates a checksum for each raw release;
3. normalizes releases with the generic OCDS adapter;
4. measures how many award cases expose Companies House identifiers (GB-COH),
   which are directly joinable to the Companies House adapter;
5. verifies that OpenIntegrity never emits an automated corruption conclusion.

It is an ingestion/joinability test, not an accusation or ranking of suppliers.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from open_integrity_agent import OpenIntegrityAgent
from source_adapters import normalize_ocds_release
from source_snapshot import make_snapshot


BASE = "https://www.find-tender.service.gov.uk/api/1.0/ocdsReleasePackages"


def fetch_package(updated_from: str, updated_to: str, limit: int = 50) -> tuple[str, dict]:
    params = {
        "updatedFrom": updated_from,
        "updatedTo": updated_to,
        "stages": "award",
        "limit": limit,
    }
    url = BASE + "?" + urlencode(params)
    req = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "ARIS4C014-OpenIntegrity/0.1 public-data-smoke",
        },
    )
    with urlopen(req, timeout=60) as response:
        return url, json.loads(response.read().decode("utf-8"))


def _parse_dt(value):
    if not value:
        return None
    return datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def analyze(package_url: str, data: dict) -> dict:
    releases = data.get("releases") or []
    agent = OpenIntegrityAgent()
    normalized_count = 0
    company_joinable_count = 0
    competition_covered_count = 0
    sample_joinable = []
    snapshots = []

    for release in releases:
        if not isinstance(release, dict):
            continue
        release_id = str(release.get("id") or release.get("ocid") or "unknown")
        snap = make_snapshot(
            release,
            source_name="UK Find a Tender OCDS",
            source_record_id=release_id,
            source_url=package_url,
            parser_version="source_adapters.py:0.2",
            published_at=_parse_dt(release.get("date")),
        )
        snapshots.append(
            {
                "record_id": snap.source_record_id,
                "published_at": snap.published_at.isoformat() if snap.published_at else None,
                "sha256": snap.sha256,
            }
        )

        imported = normalize_ocds_release(
            release,
            source_name="UK Find a Tender OCDS",
            source_url=package_url,
            jurisdiction="GB",
        )
        for case in imported.cases:
            normalized_count += 1
            if "procurement_competition" in case.source_coverage:
                competition_covered_count += 1
            supplier_ids = list(case.contract.supplier_ids)
            joinable = [x for x in supplier_ids if x.startswith("GB-COH:")]
            if joinable:
                company_joinable_count += 1
                if len(sample_joinable) < 10:
                    sample_joinable.append(
                        {
                            "contract_id": case.contract.contract_id,
                            "supplier_ids": joinable,
                            "source_coverage": sorted(case.source_coverage),
                        }
                    )
            report = agent.run(case)
            assert report["corruption_inference"] is False
            assert all(f["corruption_inference"] is False for f in report["findings"])

    return {
        "source": "UK Find a Tender",
        "endpoint": BASE,
        "release_count": len(releases),
        "normalized_award_case_count": normalized_count,
        "gb_coh_joinable_case_count": company_joinable_count,
        "competition_covered_case_count": competition_covered_count,
        "joinability_rate": (
            company_joinable_count / normalized_count if normalized_count else None
        ),
        "sample_joinable": sample_joinable,
        "raw_release_snapshots": snapshots[:10],
        "corruption_inference": False,
        "notes": [
            "GB-COH indicates direct identifier-level Companies House joinability.",
            "This smoke test does not rank or accuse suppliers.",
            "A release update window is not assumed to equal first publication time."
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="uk_fts_smoke.json")
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    end = now.replace(microsecond=0)
    start = end - timedelta(days=args.days)
    updated_from = start.strftime("%Y-%m-%dT%H:%M:%S")
    updated_to = end.strftime("%Y-%m-%dT%H:%M:%S")

    url, package = fetch_package(updated_from, updated_to)
    output = {
        "query": {
            "updated_from": updated_from,
            "updated_to": updated_to,
            "stages": "award",
            "limit": 50,
        },
        **analyze(url, package),
    }
    Path(args.out).write_text(
        json.dumps(output, indent=2, sort_keys=True), encoding="utf-8"
    )
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
