"""Build a case-enriched Sleeping Beauty mechanism cohort.

This module is intentionally different from the prospective random-cohort
benchmark.

Prospective benchmark:
    random historical cohort -> freeze at T -> predict future outcomes.

Mechanism cohort:
    large retrospective corpus -> identify robust SB cases -> construct
    normalized trajectory states -> match SBs to scientifically useful controls.

The mechanism cohort is therefore *case-enriched by design*. It must never be
used to estimate prospective prevalence or predictive performance without
appropriate sampling weights / a separate random benchmark.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Iterable, Mapping, Sequence

from mechanism_labels import (
    SCISCINET_V1_CALIBRATION,
    SourceBCalibration,
    classify_mechanism_state,
    percentile_ranks,
    post_awakening_fate,
    robust_sleeping_beauty_gate,
)
from mechanism_matching import MechanismPaper, build_priority_contrasts
from risk_set_matching import build_awakening_risk_set_contrast


@dataclass(frozen=True)
class CorpusPaper:
    paper_id: str
    publication_year: int
    field: str
    annual_citation_counts: tuple[int, ...]
    reference_count: int | None = None
    author_count: int | None = None
    source_id: str | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "paper_id": self.paper_id,
            "publication_year": self.publication_year,
            "field": self.field,
            "annual_citation_counts": list(self.annual_citation_counts),
            "reference_count": self.reference_count,
            "author_count": self.author_count,
            "source_id": self.source_id,
        }


def _validate_paper(paper: CorpusPaper) -> None:
    if not paper.paper_id:
        raise ValueError("paper_id is required")
    if not paper.field:
        raise ValueError(f"field is required for {paper.paper_id}")
    if not paper.annual_citation_counts:
        raise ValueError(f"citation history missing for {paper.paper_id}")
    if any(int(x) < 0 for x in paper.annual_citation_counts):
        raise ValueError(f"negative citation count for {paper.paper_id}")


def _early_total(counts: Sequence[int], years: int) -> int:
    return sum(int(x) for x in counts[:years])


def _late_total(counts: Sequence[int], years: int) -> int:
    return sum(int(x) for x in counts[-years:])


def build_mechanism_cohort(
    papers: Iterable[CorpusPaper],
    *,
    early_years: int = 5,
    late_years: int = 5,
    min_stratum_size: int = 20,
    b_calibration: SourceBCalibration = SCISCINET_V1_CALIBRATION,
    sb_sleep_mode: str = "VARIABLE_SLEEP",
    sb_min_sleep_years: int = 5,
    sb_fixed_sleep_years: int = 10,
    sb_max_sleep_years: int | None = None,
    sb_wake_years: int = 4,
    sb_max_sleep_rate: float = 2.0,
    sb_min_wake_rate: float = 5.0,
    sb_min_total_citations: int = 50,
    controls_per_case: int = 1,
    primary_risk_set_case_ids: set[str] | None = None,
    matching_year_tolerance: int = 0,
    matching_early_percentile_caliper: float = 0.15,
    matching_max_abs_smd: float = 0.10,
    min_primary_match_rate: float = 0.50,
    require_validated_b_calibration_for_analysis: bool = True,
) -> dict[str, Any]:
    """Create four mechanism states and primary matched contrasts.

    Normalization strata are exact (field, publication_year). Papers in strata
    below min_stratum_size are returned as ABSTAIN_STRATUM_TOO_SMALL.

    Robust SLEEPING_BEAUTY identity is determined by the retrospective
    full-trajectory gate. The normalized early/late quadrant is retained as a
    separate descriptive state and does not veto robust identity.

    Other canonical quadrant states use normalized early/late attention:
    - FORGOTTEN: low -> low
    - IMMEDIATE_HIT: high -> high
    - FADING: high -> low
    """
    rows = list(papers)
    if early_years < 1 or late_years < 1:
        raise ValueError("early_years and late_years must be >= 1")
    if min_stratum_size < 2:
        raise ValueError("min_stratum_size must be >= 2")
    if matching_max_abs_smd <= 0:
        raise ValueError("matching_max_abs_smd must be positive")
    if not 0 <= min_primary_match_rate <= 1:
        raise ValueError("min_primary_match_rate must be in [0,1]")

    for paper in rows:
        _validate_paper(paper)

    strata: dict[tuple[str, int], list[CorpusPaper]] = defaultdict(list)
    for paper in rows:
        strata[(paper.field, paper.publication_year)].append(paper)

    records: list[dict[str, Any]] = []
    matching_rows: list[MechanismPaper] = []
    state_counts: dict[str, int] = defaultdict(int)
    stratum_counts: dict[str, int] = {}

    for (field, year), members in sorted(strata.items()):
        stratum_key = f"{field}|{year}"
        stratum_counts[stratum_key] = len(members)

        if len(members) < min_stratum_size:
            for paper in members:
                records.append(
                    {
                        **paper.as_dict(),
                        "state": "ABSTAIN_STRATUM_TOO_SMALL",
                        "reason": (
                            f"stratum size {len(members)} < "
                            f"{min_stratum_size}"
                        ),
                    }
                )
                state_counts["ABSTAIN_STRATUM_TOO_SMALL"] += 1
            continue

        early_values = {
            p.paper_id: float(
                _early_total(p.annual_citation_counts, early_years)
            )
            for p in members
        }
        late_values = {
            p.paper_id: float(
                _late_total(p.annual_citation_counts, late_years)
            )
            for p in members
        }
        early_p = percentile_ranks(early_values)
        late_p = percentile_ranks(late_values)

        for paper in members:
            counts = tuple(int(x) for x in paper.annual_citation_counts)
            robust = robust_sleeping_beauty_gate(
                counts,
                b_calibration=b_calibration,
                sleep_mode=sb_sleep_mode,
                sleep_years=sb_fixed_sleep_years,
                min_sleep_years=sb_min_sleep_years,
                max_sleep_years=sb_max_sleep_years,
                wake_years=sb_wake_years,
                max_sleep_rate=sb_max_sleep_rate,
                min_wake_rate=sb_min_wake_rate,
                min_total_citations=sb_min_total_citations,
            )
            early_count = int(early_values[paper.paper_id])
            late_count = int(late_values[paper.paper_id])
            state = classify_mechanism_state(
                early_percentile=early_p[paper.paper_id],
                late_percentile=late_p[paper.paper_id],
                robust_sb=robust.robust_sb,
                early_count=early_count,
                late_count=late_count,
                zero_counts_are_low=True,
                require_robust_sb_for_sleeping_beauty=True,
            )

            post_fate = (
                post_awakening_fate(
                    counts,
                    sleep_years=robust.van_raan.sleep_years,
                    wake_years=robust.van_raan.wake_years,
                    terminal_years=late_years,
                ).as_dict()
                if robust.robust_sb
                else None
            )

            record = {
                **paper.as_dict(),
                "stratum": {
                    "field": field,
                    "publication_year": year,
                    "n": len(members),
                },
                "early_years": early_years,
                "late_years": late_years,
                "early_citation_count": early_count,
                "late_citation_count": late_count,
                "mechanism_state": state.as_dict(),
                "robust_sb_gate": robust.as_dict(),
                "post_awakening_fate": post_fate,
                "state": state.state,
            }
            records.append(record)
            state_counts[state.state] += 1

            if state.state in {
                "SLEEPING_BEAUTY",
                "FORGOTTEN",
                "IMMEDIATE_HIT",
                "FADING",
            }:
                matching_rows.append(
                    MechanismPaper(
                        paper_id=paper.paper_id,
                        state=state.state,
                        publication_year=paper.publication_year,
                        field=paper.field,
                        early_citation_percentile=early_p[paper.paper_id],
                        reference_count=paper.reference_count,
                        author_count=paper.author_count,
                        early_citation_count=early_count,
                        source_id=paper.source_id,
                        annual_citation_counts=counts,
                        robust_sleep_years=(
                            robust.van_raan.sleep_years
                            if robust.robust_sb
                            else None
                        ),
                        robust_sleep_rate=(
                            robust.van_raan.sleep_rate
                            if robust.robust_sb
                            else None
                        ),
                    )
                )

    contrasts = build_priority_contrasts(
        matching_rows,
        controls_per_case=controls_per_case,
        year_tolerance=matching_year_tolerance,
        early_percentile_caliper=matching_early_percentile_caliper,
        max_abs_smd=matching_max_abs_smd,
    )
    contrasts["SB_vs_AT_RISK_DORMANT"] = (
        build_awakening_risk_set_contrast(
            matching_rows,
            controls_per_case=controls_per_case,
            case_ids=primary_risk_set_case_ids,
            max_sleep_rate=sb_max_sleep_rate,
            wake_years=sb_wake_years,
            min_wake_rate=sb_min_wake_rate,
            max_abs_smd=matching_max_abs_smd,
        )
    )

    n_sb = state_counts.get("SLEEPING_BEAUTY", 0)
    primary = contrasts["SB_vs_AT_RISK_DORMANT"]
    primary_balance = primary["balance"]
    primary_match_ok = primary["match_rate"] >= min_primary_match_rate
    primary_balance_ok = primary_balance["balance_pass"] is True

    b_calibration_ok = (
        b_calibration.validated_for_source
        or not require_validated_b_calibration_for_analysis
    )

    mechanism_analysis_ready = (
        n_sb > 0
        and primary_match_ok
        and primary_balance_ok
        and b_calibration_ok
    )

    analysis_block_reasons = []
    if n_sb == 0:
        analysis_block_reasons.append("no robust Sleeping Beauty cases")
    if n_sb > 0 and not primary_match_ok:
        analysis_block_reasons.append(
            "SB-vs-at-risk-dormant match rate below required minimum"
        )
    if n_sb > 0 and primary_balance["balance_pass"] is None:
        analysis_block_reasons.append(
            "SB-vs-at-risk-dormant balance not assessable"
        )
    elif n_sb > 0 and primary_balance["balance_pass"] is False:
        analysis_block_reasons.append(
            "SB-vs-at-risk-dormant observed covariates remain imbalanced"
        )
    if n_sb > 0 and not b_calibration_ok:
        analysis_block_reasons.append(
            "Beauty Coefficient threshold is not validated for this source"
        )

    return {
        "dataset_type": "case-enriched mechanism cohort",
        "claim_boundary": (
            "This cohort is retrospectively enriched for robust Sleeping "
            "Beauties and matched controls. It is for mechanism comparisons, "
            "not for estimating prospective predictive performance or SB "
            "prevalence in the literature."
        ),
        "n_input_papers": len(rows),
        "n_robust_sleeping_beauties": n_sb,
        "primary_risk_set_case_ids": (
            sorted(primary_risk_set_case_ids)
            if primary_risk_set_case_ids is not None
            else None
        ),
        "state_counts": dict(sorted(state_counts.items())),
        "stratum_counts": stratum_counts,
        "definitions": {
            "normalization_stratum": "field x publication_year",
            "early_years": early_years,
            "late_years": late_years,
            "low_percentile_max": 0.25,
            "high_percentile_min": 0.75,
            "robust_sb": {
                "sleep_mode": sb_sleep_mode,
                "min_sleep_years": sb_min_sleep_years,
                "fixed_sleep_years": sb_fixed_sleep_years,
                "max_sleep_years": sb_max_sleep_years,
                "wake_years": sb_wake_years,
                "max_sleep_rate": sb_max_sleep_rate,
                "min_wake_rate": sb_min_wake_rate,
                "min_total_citations": sb_min_total_citations,
                "b_calibration": b_calibration.as_dict(),
            },
        },
        "mechanism_ready": n_sb > 0,
        "mechanism_block_reason": (
            None
            if n_sb > 0
            else (
                "No robust Sleeping Beauty cases passed the retrospective "
                "gate. Do not estimate SB mechanisms from this corpus; expand "
                "the corpus or revisit prespecified gate sensitivity."
            )
        ),
        "mechanism_analysis_ready": mechanism_analysis_ready,
        "mechanism_analysis_block_reasons": analysis_block_reasons,
        "analysis_readiness_rule": {
            "primary_contrast": "SB_vs_AT_RISK_DORMANT",
            "min_match_rate": min_primary_match_rate,
            "max_abs_smd": matching_max_abs_smd,
            "requires_assessable_balance": True,
            "requires_validated_b_calibration": (
                require_validated_b_calibration_for_analysis
            ),
            "b_calibration_validated_for_source": (
                b_calibration.validated_for_source
            ),
        },
        "contrasts": contrasts,
        "records": records,
    }


def prefilter_sciscinet_rows(
    rows: Iterable[Mapping[str, Any]],
    *,
    min_b: float = 33.0,
    min_citations: int = 50,
) -> list[Mapping[str, Any]]:
    """Cheap SciSciNet prefilter before expensive trajectory reconstruction.

    Expected fields:
    - SB_B
    - cited_by_count or Citation_Count

    Passing this prefilter does NOT make a paper a confirmed SB. Full annual
    citation histories must still pass the robust retrospective gate.
    """
    selected = []
    for row in rows:
        b = row.get("SB_B")
        citations = row.get("cited_by_count")
        if citations is None:
            citations = row.get("Citation_Count")
        if b is None or citations is None:
            continue
        if float(b) > float(min_b) and int(citations) >= int(min_citations):
            selected.append(row)
    return selected
