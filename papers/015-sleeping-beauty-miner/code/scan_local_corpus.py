"""Run a cutoff-safe baseline scan over a local SciSciNet-style slice.

This is a discovery *scaffold*. It can rank a bounded local corpus using one
transparent baseline and emit Candidate Evidence Cards, but it deliberately
does not auto-label papers as validated Sleeping Beauty candidates.

CSV/TSV works without extra dependencies. Parquet requires pandas + pyarrow
(or another pandas parquet engine).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from baselines import baseline_score, cutoff_features
from candidate_card import build_candidate_card, evidence_item
from integrity_adapter import adapt_011_findings
from sciscinet_adapter import cohort_histories, iter_citation_edges, load_paper_years


def scan(
    *,
    paper_table: str | Path,
    citation_table: str | Path,
    cutoff_year: int,
    cohort_start: int,
    cohort_end: int,
    strategy: str,
    top_k: int,
    max_targets: int | None = None,
) -> dict:
    if cohort_start > cohort_end:
        raise ValueError("cohort_start cannot exceed cohort_end")
    if cohort_end > cutoff_year:
        raise ValueError("cohort_end cannot exceed cutoff_year")
    if top_k < 1:
        raise ValueError("top_k must be >= 1")

    paper_years = load_paper_years(paper_table)
    target_ids = sorted(
        paper_id
        for paper_id, year in paper_years.items()
        if cohort_start <= year <= cohort_end
    )
    if max_targets is not None:
        target_ids = target_ids[: int(max_targets)]

    histories = cohort_histories(
        target_ids,
        paper_years=paper_years,
        citation_edges=iter_citation_edges(citation_table),
        end_year=cutoff_year,
    )

    scored: list[tuple[str, float, dict]] = []
    for paper_id in target_ids:
        history = histories[paper_id]
        features = cutoff_features(history.counts)
        score = baseline_score(features, strategy)
        scored.append((paper_id, score, features.as_dict()))

    scored.sort(key=lambda row: (-row[1], row[0]))
    selected = scored[: min(top_k, len(scored))]
    gate = adapt_011_findings([], cutoff_year=cutoff_year)

    cards = []
    for rank, (paper_id, score, features) in enumerate(selected, start=1):
        history = histories[paper_id]
        card = build_candidate_card(
            paper_id=paper_id,
            mode="DISCOVERY_SCAN",
            analysis_cutoff=cutoff_year,
            state="INSUFFICIENT_DATA",
            rank=rank,
            score=score,
            score_semantics=(
                f"Transparent exploratory baseline '{strategy}'. "
                "Not a validated future-awakening probability."
            ),
            citation_trajectory=history.as_dict(),
            evidence_families=[
                evidence_item(
                    name=f"baseline:{strategy}",
                    applicable=True,
                    cutoff_safe=True,
                    status="NEUTRAL",
                    value=features,
                    provenance=[
                        str(paper_table),
                        str(citation_table),
                        f"cutoff_year:{cutoff_year}",
                    ],
                    notes=(
                        "Baseline priority only. Additional semantic/network "
                        "evidence and empirical validation are required before "
                        "promotion to DORMANT_CANDIDATE."
                    ),
                )
            ],
            integrity_gate=gate,
            provenance=[
                str(paper_table),
                str(citation_table),
                f"cutoff_year:{cutoff_year}",
            ],
            explanation=(
                "This paper entered the shortlist under a transparent baseline "
                "scan. The reference implementation intentionally leaves its "
                "candidate state as INSUFFICIENT_DATA."
            ),
            model_version="baseline-scan-0.1",
        )
        cards.append(card)

    return {
        "mode": "DISCOVERY_SCAN",
        "cutoff_year": cutoff_year,
        "cohort": [cohort_start, cohort_end],
        "strategy": strategy,
        "n_targets": len(target_ids),
        "review_budget_k": top_k,
        "cards": cards,
        "warning": (
            "Baseline shortlist only; do not interpret ranks as validated "
            "breakthrough or scientific-validity predictions."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paper-table", required=True, type=Path)
    parser.add_argument("--citation-table", required=True, type=Path)
    parser.add_argument("--cutoff-year", required=True, type=int)
    parser.add_argument("--cohort-start", required=True, type=int)
    parser.add_argument("--cohort-end", required=True, type=int)
    parser.add_argument(
        "--strategy",
        default="dormancy",
        choices=[
            "current_citations",
            "momentum_3y",
            "acceleration_3y",
            "partial_beauty",
            "dormancy",
        ],
    )
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--max-targets", type=int)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = scan(
        paper_table=args.paper_table,
        citation_table=args.citation_table,
        cutoff_year=args.cutoff_year,
        cohort_start=args.cohort_start,
        cohort_end=args.cohort_end,
        strategy=args.strategy,
        top_k=args.top_k,
        max_targets=args.max_targets,
    )
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
