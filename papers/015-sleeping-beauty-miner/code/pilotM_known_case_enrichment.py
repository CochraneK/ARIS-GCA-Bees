"""Case-enriched real-data mechanism pilot for ARIS4C015.

Three literature-reference Sleeping Beauties already replicated in Pilot 0 are
inserted as cases. For each case, controls are sampled from the same
publication year and current OpenAlex primary field.

This is a mechanism-plumbing / matched-control pilot. It is not a population
prevalence study and the OpenAlex B threshold remains provisional.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from mechanism_cohort import CorpusPaper, build_mechanism_cohort
from mechanism_labels import OPENALEX_PROVISIONAL_CALIBRATION
from openalex_adapter import (
    OpenAlexError,
    fetch_work,
    reconstruct_history_for_known_work,
    sample_works,
)


KNOWN_CASES = (
    {
        "case_id": "ke2015_02_hummers",
        "doi": "10.1021/ja01539a017",
        "publication_year": 1958,
        "published_b": 10769.0,
        "published_awakening_year": 2007,
        "seed": 2158,
    },
    {
        "case_id": "ke2015_06_epr",
        "doi": "10.1103/PhysRev.47.777",
        "publication_year": 1935,
        "published_b": 2258.0,
        "published_awakening_year": 1994,
        "seed": 61935,
    },
    {
        "case_id": "ke2015_07_washburn",
        "doi": "10.1103/PhysRev.17.273",
        "publication_year": 1921,
        "published_b": 2184.0,
        "published_awakening_year": 1995,
        "seed": 71921,
    },
)


def _sample_unique_control_pool(
    *,
    filters: str,
    target_size: int,
    base_seed: int,
    api_key: str | None,
    exclude_ids: set[str] | None = None,
) -> tuple[list, dict[str, Any]]:
    """Build a deterministic unique OpenAlex control pool across seed pages.

    OpenAlex one-page random sampling is capped at 100 works. For larger
    mechanism reservoirs, issue deterministic independent sample pages and
    deduplicate by OpenAlex ID. The first page uses the historical base seed,
    so targets <=100 preserve the original sampling convention.
    """
    if target_size < 1 or target_size > 1000:
        raise ValueError("target_size must be between 1 and 1000")

    excluded = set(exclude_ids or ())
    selected = []
    selected_ids: set[str] = set()
    attempts = []
    round_index = 0
    max_rounds = max(10, ((target_size + 99) // 100) * 4)

    while len(selected) < target_size and round_index < max_rounds:
        remaining = target_size - len(selected)
        request_size = min(100, remaining)
        seed = int(base_seed) + round_index * 104729
        sampled = sample_works(
            filters=filters,
            sample_size=request_size,
            seed=seed,
            api_key=api_key,
        )
        accepted = 0
        for work in sampled:
            work_id = getattr(work, "openalex_id", None)
            if not work_id or work_id in excluded or work_id in selected_ids:
                continue
            selected.append(work)
            selected_ids.add(work_id)
            accepted += 1
            if len(selected) >= target_size:
                break
        attempts.append(
            {
                "seed": seed,
                "requested": request_size,
                "returned": len(sampled),
                "accepted_unique": accepted,
            }
        )
        round_index += 1

    if len(selected) < target_size:
        raise OpenAlexError(
            "Could not assemble requested unique control pool: "
            f"target={target_size}, unique={len(selected)}, "
            f"attempts={round_index}"
        )

    return selected, {
        "target_size": target_size,
        "unique_size": len(selected),
        "base_seed": int(base_seed),
        "seed_stride": 104729,
        "attempts": attempts,
    }


def _corpus_paper(
    work,
    history,
    *,
    field_label: str,
) -> CorpusPaper:
    return CorpusPaper(
        paper_id=work.openalex_id,
        publication_year=int(work.publication_year),
        field=field_label,
        annual_citation_counts=history.counts,
        reference_count=work.referenced_works_count,
        author_count=work.authorship_count,
        source_id=None,
    )


def run_known_case_enrichment(
    *,
    controls_per_case_pool: int = 50,
    matched_controls_per_case: int = 1,
    observation_end_year: int = 2011,
    api_key: str | None = None,
) -> dict[str, Any]:
    if controls_per_case_pool < 20 or controls_per_case_pool > 1000:
        raise ValueError("controls_per_case_pool must be between 20 and 1000")
    if matched_controls_per_case < 1 or matched_controls_per_case > 10:
        raise ValueError("matched_controls_per_case must be between 1 and 10")

    papers: list[CorpusPaper] = []
    known_case_meta = []
    control_meta = []
    control_sampling_meta = []
    seen_ids: set[str] = set()

    for spec in KNOWN_CASES:
        identifier = f"https://doi.org/{spec['doi']}"
        case_work = fetch_work(identifier, api_key=api_key)
        if case_work.publication_year is None:
            raise OpenAlexError(f"{spec['case_id']} has no publication year")
        if case_work.primary_field_id is None:
            raise OpenAlexError(f"{spec['case_id']} has no primary field")

        year = int(spec["publication_year"])
        field_id = case_work.primary_field_id
        field_label = f"OPENALEX_FIELD_{field_id}"

        case_history = reconstruct_history_for_known_work(
            case_work,
            publication_year=year,
            end_year=observation_end_year,
            api_key=api_key,
            max_records=None,
        )
        papers.append(
            _corpus_paper(
                case_work,
                case_history,
                field_label=field_label,
            )
        )
        seen_ids.add(case_work.openalex_id)

        known_case_meta.append(
            {
                **spec,
                "openalex_id": case_work.openalex_id,
                "title": case_work.title,
                "primary_topic": case_work.primary_topic,
                "primary_field_id": field_id,
                "reference_count": case_work.referenced_works_count,
                "author_count": case_work.authorship_count,
                "citations_through_endpoint": case_history.total_citations,
            }
        )

        filters = (
            f"publication_year:{year},type:article,"
            f"primary_topic.field.id:{field_id}"
        )
        sampled, sampling_meta = _sample_unique_control_pool(
            filters=filters,
            target_size=controls_per_case_pool,
            base_seed=int(spec["seed"]),
            api_key=api_key,
            exclude_ids=seen_ids,
        )
        control_sampling_meta.append(
            {
                "case_id": spec["case_id"],
                "publication_year": year,
                "field_id": field_id,
                **sampling_meta,
            }
        )

        for control in sampled:
            if not control.openalex_id:
                continue
            if control.openalex_id in seen_ids:
                continue
            if control.publication_year is None:
                continue

            history = reconstruct_history_for_known_work(
                control,
                publication_year=year,
                end_year=observation_end_year,
                api_key=api_key,
                max_records=None,
            )
            papers.append(
                _corpus_paper(
                    control,
                    history,
                    field_label=field_label,
                )
            )
            seen_ids.add(control.openalex_id)
            control_meta.append(
                {
                    "paper_id": control.openalex_id,
                    "title": control.title,
                    "doi": control.doi,
                    "publication_year": year,
                    "field_id": field_id,
                    "primary_topic": control.primary_topic,
                    "citations_through_endpoint": history.total_citations,
                }
            )

    min_stratum_size = max(20, min(40, controls_per_case_pool - 5))
    result = build_mechanism_cohort(
        papers,
        min_stratum_size=min_stratum_size,
        b_calibration=OPENALEX_PROVISIONAL_CALIBRATION,
        sb_sleep_mode="VARIABLE_SLEEP",
        sb_min_sleep_years=5,
        sb_wake_years=4,
        sb_max_sleep_rate=2.0,
        sb_min_wake_rate=5.0,
        sb_min_total_citations=50,
        controls_per_case=matched_controls_per_case,
        matching_early_percentile_caliper=0.15,
        matching_max_abs_smd=0.10,
        min_primary_match_rate=0.50,
        require_validated_b_calibration_for_analysis=True,
    )

    by_id = {
        row["paper_id"]: row
        for row in result["records"]
        if row.get("paper_id")
    }
    case_assessment = []
    for meta in known_case_meta:
        record = by_id.get(meta["openalex_id"])
        case_assessment.append(
            {
                **meta,
                "mechanism_state": (
                    record.get("state") if record else "MISSING_RECORD"
                ),
                "relative_quadrant": (
                    (record.get("mechanism_state") or {}).get(
                        "quadrant_state"
                    )
                    if record
                    else None
                ),
                "post_awakening_fate": (
                    record.get("post_awakening_fate")
                    if record
                    else None
                ),
                "robust_sb_gate": (
                    record.get("robust_sb_gate") if record else None
                ),
                "early_citation_count": (
                    record.get("early_citation_count") if record else None
                ),
                "late_citation_count": (
                    record.get("late_citation_count") if record else None
                ),
            }
        )

    result["pilot_design"] = {
        "type": "literature-known case-enriched matched-control smoke",
        "known_case_source": "Ke et al. 2015 PNAS",
        "n_known_cases": len(KNOWN_CASES),
        "controls_per_case_pool_requested": controls_per_case_pool,
        "matched_controls_per_case": matched_controls_per_case,
        "control_sampling": control_sampling_meta,
        "observation_end_year": observation_end_year,
        "control_frame": "same publication year x current OpenAlex primary field",
        "case_selection_is_retrospective": True,
        "population_prevalence_estimable": False,
        "openalex_b_calibration_validated": False,
    }
    result["known_case_assessment"] = case_assessment
    result["control_metadata"] = control_meta
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls-per-case-pool", type=int, default=50)
    parser.add_argument("--matched-controls-per-case", type=int, default=1)
    parser.add_argument("--observation-end-year", type=int, default=2011)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_known_case_enrichment(
        controls_per_case_pool=args.controls_per_case_pool,
        matched_controls_per_case=args.matched_controls_per_case,
        observation_end_year=args.observation_end_year,
        api_key=args.api_key,
    )
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
