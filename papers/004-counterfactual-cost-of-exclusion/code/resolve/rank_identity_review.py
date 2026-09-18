#!/usr/bin/env python3
"""Rank MH-blind ARIS4C004 identity-review packets for efficient adjudication.

This is a triage aid, not an identity classifier. It never assigns VERIFIED_*.
The ranking uses only identity/network observability evidence already available
before mental-health coding.

Priority intuition:
- single plausible records before fragmented clusters;
- stronger external authority context before sparse authority context;
- lower temporal contamination before heavily contaminated records;
- clear no-graph/collision states require less active adjudication and are lower
  priority unless a reviewer explicitly reopens them.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def read_existing(path: Path | None) -> set[str]:
    if not path or not path.exists():
        return set()
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return {row["person_id"] for row in csv.DictReader(handle)}


def authority_strength(authority: dict[str, Any]) -> int:
    score = 0
    if authority.get("orcid"):
        score += 5
    if authority.get("viaf") or authority.get("isni") or authority.get("gnd") or authority.get("loc"):
        score += 3
    if authority.get("notable_works"):
        score += 3
    if authority.get("occupations") or authority.get("fields_of_work"):
        score += 2
    if authority.get("employers") or authority.get("educated_at"):
        score += 1
    return score


def contamination_fraction(profile: dict[str, Any]) -> float | None:
    contamination = profile.get("contamination") or {}
    for key in (
        "outside_fraction",
        "outside_window_fraction",
        "outside_share",
    ):
        value = contamination.get(key)
        if value is not None:
            try:
                return float(value)
            except (TypeError, ValueError):
                pass
    plausible = contamination.get("plausible_work_n")
    outside = contamination.get("outside_work_n")
    try:
        plausible_i = int(plausible)
        outside_i = int(outside)
        total = plausible_i + outside_i
        return outside_i / total if total else None
    except (TypeError, ValueError):
        return None


def rank_packet(packet: dict[str, Any]) -> dict[str, Any]:
    review_class = str(packet.get("review_class") or "")
    authority = packet.get("authority_evidence") or {}
    profiles = packet.get("openalex_profiles") or []
    plausible_ids = packet.get("plausible_openalex_ids") or []

    class_base = {
        "single_plausible_author_record": 100,
        "single_low_confidence_record": 75,
        "possible_author_fragmentation": 60,
        "possible_name_collision_conflicting_orcid": 20,
        "name_collision_or_low_similarity": 15,
        "no_openalex_search_hit": 5,
    }.get(review_class, 40)

    auth = authority_strength(authority)
    contaminations = [
        x for x in (contamination_fraction(profile) for profile in profiles)
        if x is not None
    ]
    best_contam = min(contaminations) if contaminations else None
    contam_bonus = 0
    if best_contam is not None:
        if best_contam <= 0.10:
            contam_bonus = 15
        elif best_contam <= 0.30:
            contam_bonus = 8
        elif best_contam >= 0.70:
            contam_bonus = -15

    profile_bonus = 5 if profiles else 0
    fragmentation_penalty = max(0, len(plausible_ids) - 1) * 2
    score = class_base + auth + contam_bonus + profile_bonus - fragmentation_penalty

    if review_class == "no_openalex_search_hit":
        bucket = "closed_no_graph"
    elif "collision" in review_class:
        bucket = "collision_review"
    elif review_class == "single_plausible_author_record":
        bucket = "single_first"
    elif review_class == "single_low_confidence_record":
        bucket = "single_low_confidence"
    elif review_class == "possible_author_fragmentation":
        bucket = "cluster_review"
    else:
        bucket = "other_review"

    return {
        "person_id": str(packet.get("person_id") or ""),
        "canonical_name": str(packet.get("canonical_name") or ""),
        "birth_year": packet.get("birth_year") or "",
        "death_year": packet.get("death_year") or "",
        "review_class": review_class,
        "priority_bucket": bucket,
        "priority_score": score,
        "authority_strength_score": auth,
        "profile_n": len(profiles),
        "plausible_openalex_id_n": len(plausible_ids),
        "best_temporal_contamination_fraction": (
            round(best_contam, 6) if best_contam is not None else ""
        ),
        "suggested_nonfinal_status": packet.get("suggested_nonfinal_status") or "",
        "mental_health_evidence_used": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("packet_jsonl", type=Path)
    parser.add_argument("--existing-reviewed", type=Path)
    parser.add_argument("--output-csv", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    args = parser.parse_args()

    existing = read_existing(args.existing_reviewed)
    ranked = [
        rank_packet(packet)
        for packet in read_jsonl(args.packet_jsonl)
        if str(packet.get("person_id") or "") not in existing
    ]
    ranked.sort(
        key=lambda row: (
            -int(row["priority_score"]),
            row["priority_bucket"],
            row["canonical_name"],
        )
    )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = list(ranked[0].keys()) if ranked else [
        "person_id",
        "canonical_name",
        "priority_score",
    ]
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(ranked)

    bucket_counts: dict[str, int] = {}
    for row in ranked:
        bucket = str(row["priority_bucket"])
        bucket_counts[bucket] = bucket_counts.get(bucket, 0) + 1
    summary = {
        "unreviewed_people_n": len(ranked),
        "priority_bucket_counts": bucket_counts,
        "mental_health_information_used": False,
        "warning": "Priority is workflow triage only and must never be interpreted as identity confidence or scientific importance.",
    }
    args.summary_json.write_text(
        json.dumps(summary, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
