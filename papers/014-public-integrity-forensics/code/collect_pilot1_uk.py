"""Frozen-window collector for ARIS4C014 UK Pilot 1A.

This collector is deliberately narrow:
- only official FTS and Contracts Finder OCDS award-stage search endpoints;
- fixed dates from a committed config;
- raw package + per-release SHA-256 snapshots saved to workflow artifact;
- normalized coverage summaries contain identifiers/counts, not person names;
- no Companies House API call until a key is supplied separately.

It measures source and identifier coverage, not corruption.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from source_adapters import normalize_ocds_release
from source_snapshot import make_snapshot


def get_json(url: str) -> dict:
    req = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "ARIS4C014-OpenIntegrity/0.1 frozen-pilot1",
        },
    )
    with urlopen(req, timeout=90) as response:
        return json.loads(response.read().decode("utf-8-sig"))


def parse_dt(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def build_url(source_key: str, spec: dict, window: dict) -> str:
    start = parse_dt(window["start"])
    end = parse_dt(window["end"])
    if source_key == "find_a_tender":
        params = {
            "updatedFrom": start.strftime("%Y-%m-%dT%H:%M:%S"),
            "updatedTo": end.strftime("%Y-%m-%dT%H:%M:%S"),
            "stages": spec["stages"],
            "limit": spec["limit"],
        }
    elif source_key == "contracts_finder":
        params = {
            "publishedFrom": start.strftime("%Y-%m-%d"),
            "publishedTo": end.strftime("%Y-%m-%d"),
            "stages": spec["stages"],
            "limit": spec["limit"],
        }
    else:
        raise ValueError(f"unsupported source: {source_key}")
    return spec["endpoint"] + "?" + urlencode(params)


def source_name(source_key: str) -> str:
    return {
        "find_a_tender": "UK Find a Tender OCDS",
        "contracts_finder": "UK Contracts Finder OCDS",
    }[source_key]


def collect_source(source_key: str, spec: dict, window: dict, raw_dir: Path) -> dict:
    url = build_url(source_key, spec, window)
    package = get_json(url)
    raw_path = raw_dir / f"{source_key}_release_package.json"
    raw_path.write_text(
        json.dumps(package, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8",
    )

    releases = package.get("releases") or []
    snapshots = []
    case_count = 0
    joinable_count = 0
    competition_count = 0
    stable_supplier_count = 0
    warning_count = 0
    joinable_contract_ids = []

    retrieved = datetime.now(timezone.utc)
    for release in releases:
        if not isinstance(release, dict):
            continue
        rid = str(release.get("id") or release.get("ocid") or "unknown")
        pub = None
        if release.get("date"):
            try:
                pub = parse_dt(str(release["date"]))
            except ValueError:
                pub = None
        snap = make_snapshot(
            release,
            source_name=source_name(source_key),
            source_record_id=rid,
            source_url=url,
            parser_version="source_adapters.py:0.3",
            retrieved_at=retrieved,
            published_at=pub,
        )
        snapshots.append(snap.to_dict())

        imported = normalize_ocds_release(
            release,
            source_name=source_name(source_key),
            source_url=url,
            jurisdiction="GB",
            retrieved_at=retrieved.date(),
        )
        warning_count += len(imported.warnings)
        for case in imported.cases:
            case_count += 1
            supplier_ids = list(case.contract.supplier_ids)
            stable_supplier_count += sum(":" in x for x in supplier_ids)
            joinable = [x for x in supplier_ids if x.startswith("GB-COH:")]
            if joinable:
                joinable_count += 1
                if len(joinable_contract_ids) < 25:
                    joinable_contract_ids.append(case.contract.contract_id)
            if "procurement_competition" in case.source_coverage:
                competition_count += 1

    return {
        "source_key": source_key,
        "source_name": source_name(source_key),
        "query_url": url,
        "release_count": len(releases),
        "award_case_count": case_count,
        "gb_coh_joinable_case_count": joinable_count,
        "gb_coh_joinability_rate": joinable_count / case_count if case_count else None,
        "competition_covered_case_count": competition_count,
        "competition_coverage_rate": competition_count / case_count if case_count else None,
        "stable_supplier_identifier_occurrences": stable_supplier_count,
        "adapter_warning_count": warning_count,
        "sample_joinable_contract_ids": joinable_contract_ids,
        "raw_file": raw_path.name,
        "release_snapshots": snapshots,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--out-dir", required=True)
    args = parser.parse_args()

    config = json.loads(Path(args.config).read_text(encoding="utf-8"))
    out_dir = Path(args.out_dir)
    raw_dir = out_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for key, spec in config["sources"].items():
        results.append(collect_source(key, spec, config["window"], raw_dir))

    manifest = {
        "pilot_id": config["pilot_id"],
        "frozen_on": config["frozen_on"],
        "window": config["window"],
        "purpose": config["purpose"],
        "collection_completed_at": datetime.now(timezone.utc).isoformat(),
        "join_policy": config["join_policy"],
        "sources": results,
        "totals": {
            "award_case_count": sum(x["award_case_count"] for x in results),
            "gb_coh_joinable_case_count": sum(
                x["gb_coh_joinable_case_count"] for x in results
            ),
            "competition_covered_case_count": sum(
                x["competition_covered_case_count"] for x in results
            ),
        },
        "corruption_inference": False,
        "limitations": [
            "This is a bounded source-feasibility collection, not a population estimate.",
            "Source overlap is not de-duplicated across FTS and Contracts Finder in the totals.",
            "No person-name join is performed.",
            "Companies House live enrichment is intentionally outside this collection until authenticated API access is supplied.",
            "Missing bidder counts remain missing and do not become negative or positive integrity findings."
        ],
    }
    (out_dir / "pilot1_uk_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({
        "pilot_id": manifest["pilot_id"],
        "window": manifest["window"],
        "totals": manifest["totals"],
        "by_source": [
            {
                "source": x["source_name"],
                "release_count": x["release_count"],
                "award_case_count": x["award_case_count"],
                "gb_coh_joinable_case_count": x["gb_coh_joinable_case_count"],
                "gb_coh_joinability_rate": x["gb_coh_joinability_rate"],
                "competition_covered_case_count": x["competition_covered_case_count"],
            } for x in results
        ],
        "corruption_inference": False
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
