#!/usr/bin/env python3
"""Assemble an auditable, mental-health-blind identity review packet.

Combines:
- frozen candidate metadata;
- OpenAlex search/fragment review queue;
- author profiles and representative works;
- guarded pairwise fragment evidence;
- independent Wikidata authority/bibliographic context.

The packet proposes only PROVISIONAL/NO_GRAPH/COLLISION states. It never creates
VERIFIED_SINGLE or VERIFIED_CLUSTER automatically.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def by_key(rows: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(row.get(key) or ""): row for row in rows if row.get(key)}


def group_by(rows: list[dict[str, Any]], key: str) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get(key) or "")].append(row)
    return grouped


def suggested_status(review_class: str) -> str:
    mapping = {
        "possible_author_fragmentation": "PROVISIONAL_CLUSTER",
        "single_plausible_author_record": "PROVISIONAL_SINGLE",
        "single_low_confidence_record": "PROVISIONAL_SINGLE",
        "no_openalex_search_hit": "NO_GRAPH_RECORD",
        "name_collision_or_low_similarity": "AMBIGUOUS_COLLISION",
        "possible_name_collision_conflicting_orcid": "AMBIGUOUS_COLLISION",
    }
    return mapping.get(review_class, "PROVISIONAL_SINGLE")


def compact_authority(authority: dict[str, Any]) -> dict[str, Any]:
    keys = [
        "wikidata_label",
        "wikidata_description",
        "aliases",
        "occupations",
        "fields_of_work",
        "employers",
        "educated_at",
        "notable_works",
        "member_of",
        "academic_degrees",
        "orcid",
        "viaf",
        "isni",
        "gnd",
        "loc",
    ]
    return {key: authority.get(key, [] if key not in {"wikidata_label", "wikidata_description"} else "") for key in keys}


def markdown_value(items: Any, max_items: int = 8) -> str:
    if items is None or items == "":
        return "—"
    if isinstance(items, str):
        return items or "—"
    if isinstance(items, list):
        rendered: list[str] = []
        for item in items[:max_items]:
            if isinstance(item, dict):
                label = item.get("label") or item.get("title") or item.get("id") or item.get("qid")
                qid = item.get("qid")
                rendered.append(f"{label} ({qid})" if qid and label != qid else str(label))
            else:
                rendered.append(str(item))
        suffix = f" … +{len(items)-max_items}" if len(items) > max_items else ""
        return "; ".join(rendered) + suffix if rendered else "—"
    return str(items)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--profiles", type=Path, required=True)
    parser.add_argument("--guarded-pairs", type=Path, required=True)
    parser.add_argument("--authority", type=Path, required=True)
    parser.add_argument("--output-jsonl", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    parser.add_argument("--summary-json", type=Path, required=True)
    parser.add_argument("--max-candidates", type=int, default=30)
    args = parser.parse_args()

    candidates = read_csv(args.candidates)[: args.max_candidates]
    queue = by_key(read_csv(args.queue), "person_id")
    profiles = group_by(read_jsonl(args.profiles), "person_id")
    pairs = group_by(read_jsonl(args.guarded_pairs), "person_id")
    authority = by_key(read_jsonl(args.authority), "person_id")

    packets: list[dict[str, Any]] = []
    for candidate in candidates:
        pid = candidate.get("person_id", "")
        q = queue.get(pid, {})
        review_class = q.get("review_class", "no_openalex_search_hit")
        packet = {
            "person_id": pid,
            "canonical_name": candidate.get("canonical_name", ""),
            "wikidata_qid": candidate.get("wikidata_qid", ""),
            "birth_year": candidate.get("birth_year", ""),
            "death_year": candidate.get("death_year", ""),
            "source_occupation": candidate.get("level3_main_occ", ""),
            "source_region": candidate.get("region", ""),
            "pilot_stratum": candidate.get("pilot_stratum", ""),
            "review_class": review_class,
            "suggested_nonfinal_status": suggested_status(review_class),
            "plausible_openalex_ids": [x for x in (q.get("plausible_openalex_ids") or "").split(";") if x],
            "openalex_profiles": profiles.get(pid, []),
            "guarded_fragment_pairs": pairs.get(pid, []),
            "authority_evidence": compact_authority(authority.get(pid, {})),
            "final_identity_status": None,
            "reviewer_decision_required": True,
            "mental_health_evidence_used": False,
        }
        packets.append(packet)

    args.output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with args.output_jsonl.open("w", encoding="utf-8") as handle:
        for packet in packets:
            handle.write(json.dumps(packet, ensure_ascii=False) + "\n")

    md: list[str] = [
        "# ARIS4C004 identity review packet",
        "",
        "**Pre-exposure / mental-health-blind.** Suggested states are non-final; only human/external review may assign VERIFIED_SINGLE or VERIFIED_CLUSTER.",
        "",
    ]
    for i, packet in enumerate(packets, start=1):
        auth = packet["authority_evidence"]
        md.extend(
            [
                f"## {i}. {packet['canonical_name']}",
                "",
                f"- Person ID: `{packet['person_id']}` · Wikidata `{packet['wikidata_qid']}`",
                f"- Lifespan: {packet['birth_year']}–{packet['death_year']} · source occupation: **{packet['source_occupation'] or '—'}** · region: {packet['source_region'] or '—'}",
                f"- OpenAlex review class: `{packet['review_class']}` → non-final suggestion `{packet['suggested_nonfinal_status']}`",
                f"- Wikidata description: {auth.get('wikidata_description') or '—'}",
                f"- Occupations: {markdown_value(auth.get('occupations'))}",
                f"- Fields of work: {markdown_value(auth.get('fields_of_work'))}",
                f"- Employers: {markdown_value(auth.get('employers'))}",
                f"- Educated at: {markdown_value(auth.get('educated_at'))}",
                f"- Notable works: {markdown_value(auth.get('notable_works'))}",
                f"- Authority IDs: ORCID={markdown_value(auth.get('orcid'))}; VIAF={markdown_value(auth.get('viaf'))}; ISNI={markdown_value(auth.get('isni'))}; GND={markdown_value(auth.get('gnd'))}; LoC={markdown_value(auth.get('loc'))}",
                "",
            ]
        )
        profile_rows = packet["openalex_profiles"]
        if profile_rows:
            md.append("### Plausible OpenAlex records")
            md.append("")
            for profile in profile_rows:
                c = profile.get("contamination") or {}
                md.append(
                    f"- `{profile.get('author_id')}` **{profile.get('display_name') or ''}** — plausible works {c.get('plausible_works_n', 0)}, outside-window share {c.get('outside_window_share')}; years {c.get('all_year_min')}–{c.get('all_year_max')}"
                )
                for work in (profile.get("representative_plausible_works") or [])[:3]:
                    md.append(
                        f"  - {work.get('year')}: {work.get('title') or 'untitled'}{f' · {work.get("doi")}' if work.get('doi') else ''}"
                    )
            md.append("")
        pair_rows = packet["guarded_fragment_pairs"]
        if pair_rows:
            md.append("### Fragment-pair evidence")
            md.append("")
            for pair in pair_rows:
                md.append(
                    f"- `{pair.get('author_id_a')}` ↔ `{pair.get('author_id_b')}`: **{pair.get('guarded_review_label')}** (raw={pair.get('raw_review_label')}; anchors={', '.join(pair.get('identity_anchor_reasons') or []) or 'none'}; conflicts={', '.join(pair.get('conflict_reasons') or []) or 'none'})"
                )
            md.append("")
        md.extend(["**Reviewer decision:** _pending_", "", "---", ""])

    args.output_md.write_text("\n".join(md), encoding="utf-8")

    counts: dict[str, int] = {}
    for packet in packets:
        key = packet["suggested_nonfinal_status"]
        counts[key] = counts.get(key, 0) + 1
    summary = {
        "packet_candidates_n": len(packets),
        "nonfinal_status_counts": counts,
        "with_authority_evidence_n": sum(
            bool((p["authority_evidence"].get("occupations") or p["authority_evidence"].get("fields_of_work") or p["authority_evidence"].get("viaf")))
            for p in packets
        ),
        "final_verified_n": 0,
        "mental_health_evidence_used": False,
        "note": "Packet suggestions are triage only and cannot enter confirmatory analysis as verified identities.",
    }
    args.summary_json.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
