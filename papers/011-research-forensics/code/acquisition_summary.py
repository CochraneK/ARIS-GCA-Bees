"""Summarise Track-A historical-artifact readiness at issue level."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ISSUE_STATUSES = {
    "CONTENT_ELIGIBLE",
    "CONTENT_INELIGIBLE",
    "ADJUDICATION_REQUIRED",
}


def _split_roles(value: str) -> List[str]:
    return [x.strip() for x in str(value or "").split(";") if x.strip()]


def index_objects(rows: Iterable[Dict[str, str]]) -> Dict[Tuple[str, str], List[str]]:
    index: Dict[Tuple[str, str], List[str]] = defaultdict(list)
    for row in rows:
        index[(row["target_doi"].strip(), row["object_role"].strip())].append(
            row["status"].strip()
        )
    return dict(index)


def summarize_issue(
    requirement: Dict[str, str],
    object_index: Dict[Tuple[str, str], List[str]],
) -> Dict[str, str]:
    doi = requirement["target_doi"].strip()
    issue_status = requirement["track_a_issue_status"].strip()
    if issue_status not in ISSUE_STATUSES:
        raise ValueError(f"Unknown track_a_issue_status: {issue_status}")

    base = {
        "target_doi": doi,
        "issue_code": requirement["issue_code"].strip(),
        "stratum": requirement["stratum"].strip(),
        "ground_truth_tier": requirement["ground_truth_tier"].strip(),
        "track_a_issue_status": issue_status,
        "required_roles": requirement.get("required_roles", "").strip(),
        "exact_roles": "",
        "proxy_roles": "",
        "unavailable_roles": "",
        "role_states": "",
        "issue_readiness": "",
    }

    if issue_status == "CONTENT_INELIGIBLE":
        base["issue_readiness"] = "TRACK_A_INELIGIBLE_CONTENT"
        return base

    if issue_status == "ADJUDICATION_REQUIRED":
        base["issue_readiness"] = "ADJUDICATION_REQUIRED"
        return base

    roles = _split_roles(requirement.get("required_roles", ""))
    if not roles:
        raise ValueError(f"CONTENT_ELIGIBLE issue {doi} has no required_roles")

    exact: List[str] = []
    proxy: List[str] = []
    unavailable: List[str] = []
    role_states: List[str] = []

    for role in roles:
        statuses = object_index.get((doi, role), [])
        if "SAFE_EXACT" in statuses:
            exact.append(role)
            state = "SAFE_EXACT"
        elif "PROXY_ONLY" in statuses:
            proxy.append(role)
            state = "PROXY_ONLY"
        elif statuses:
            unavailable.append(role)
            state = "+".join(sorted(set(statuses)))
        else:
            unavailable.append(role)
            state = "NO_OBJECT"
        role_states.append(f"{role}:{state}")

    base["exact_roles"] = ";".join(exact)
    base["proxy_roles"] = ";".join(proxy)
    base["unavailable_roles"] = ";".join(unavailable)
    base["role_states"] = ";".join(role_states)

    if unavailable:
        base["issue_readiness"] = "BLOCKED_REQUIRED_ROLE"
    elif proxy:
        base["issue_readiness"] = "PROXY_ONLY"
    else:
        base["issue_readiness"] = "SAFE_EXACT_READY"

    return base


def summarize_all(
    requirements: Iterable[Dict[str, str]],
    objects: Iterable[Dict[str, str]],
) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
    reqs = list(requirements)
    objs = list(objects)
    index = index_objects(objs)
    rows = [summarize_issue(req, index) for req in reqs]

    eligible = [r for r in rows if r["track_a_issue_status"] == "CONTENT_ELIGIBLE"]
    safe_targets = {
        row["target_doi"].strip()
        for row in objs
        if row["status"].strip() == "SAFE_EXACT"
    }

    summary = {
        "seed_issue_count": len(rows),
        "content_eligible_issue_count": len(eligible),
        "content_ineligible_issue_count": sum(
            r["track_a_issue_status"] == "CONTENT_INELIGIBLE" for r in rows
        ),
        "adjudication_required_issue_count": sum(
            r["track_a_issue_status"] == "ADJUDICATION_REQUIRED" for r in rows
        ),
        "safe_exact_issue_ready_count": sum(
            r["issue_readiness"] == "SAFE_EXACT_READY" for r in eligible
        ),
        "proxy_only_issue_ready_count": sum(
            r["issue_readiness"] == "PROXY_ONLY" for r in eligible
        ),
        "blocked_required_role_count": sum(
            r["issue_readiness"] == "BLOCKED_REQUIRED_ROLE" for r in eligible
        ),
        "targets_with_any_safe_exact_object": len(safe_targets),
    }
    return rows, summary


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(rows: List[Dict[str, str]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError("No readiness rows to write")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--requirements", required=True, type=Path)
    parser.add_argument("--objects", required=True, type=Path)
    parser.add_argument("--output-csv", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    args = parser.parse_args()

    rows, summary = summarize_all(
        read_csv(args.requirements),
        read_csv(args.objects),
    )
    write_csv(rows, args.output_csv)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
