"""Pilot 1 lexical-novelty ablation for ARIS4C015.

This runner evaluates a first non-citation feature family against the exact
same future outcomes used by the citation baselines.

Target inputs are self-contained Pilot 1 cohort artifacts. They already include
future outcome labels, so this script does not query target citation histories.

Historical prior corpus
-----------------------
For a target publication cohort Y, the caller supplies a prior-corpus filter
covering only years before Y. The live wrapper samples prior titles from
OpenAlex with a fixed seed. Only titles are used to construct lexical novelty.

Signals
-------
- lexical_nearest1_distance
- lexical_nearest3_distance
- lexical_oov_share

They remain separate. No arbitrary weighted lexical-novelty composite is
introduced.

Important caveat
----------------
Current OpenAlex primary-field assignments may define exploratory target/prior
strata. They are not used as predictor values and must be audited before
confirmatory historical claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from external_feature_eval import evaluate_feature_outcome_matrix
from lexical_novelty import batch_title_novelty
from openalex_adapter import sample_works


OUTCOME_TYPES = {
    "beauty_percentile": "graded",
    "beauty_top_fraction": "binary",
    "future_acceleration_percentile": "graded",
    "future_uptake_percentile": "graded",
    "awakening_within_horizon": "binary",
    "delayed_recognition_consensus": "binary",
    "delayed_recognition_with_uptake_floor": "binary",
}


def _hash_ids(ids: Sequence[str]) -> str:
    return hashlib.sha256(
        "\n".join(sorted(ids)).encode("utf-8")
    ).hexdigest()


def _outcomes_from_cohort(
    cohort: Mapping[str, Any],
) -> dict[str, tuple[str, dict[str, float]]]:
    cases = cohort.get("cases") or []
    result: dict[str, tuple[str, dict[str, float]]] = {}
    for outcome_name, kind in OUTCOME_TYPES.items():
        values: dict[str, float] = {}
        for case in cases:
            outcomes = case.get("outcomes") or {}
            if outcome_name in outcomes:
                values[str(case["paper_id"])] = float(
                    outcomes[outcome_name]
                )
        if values:
            result[outcome_name] = (kind, values)
    return result


def evaluate_lexical_ablation(
    cohort: Mapping[str, Any],
    *,
    prior_titles: Sequence[str | None],
    prior_ids: Sequence[str] | None = None,
    prior_provenance: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate lexical novelty against a frozen Pilot 1 cohort artifact."""
    cases = cohort.get("cases") or []
    if not cases:
        raise ValueError("cohort artifact contains no cases")
    if not prior_titles:
        raise ValueError("prior title corpus is empty")

    targets = {
        str(case["paper_id"]): case.get("title")
        for case in cases
    }
    features = batch_title_novelty(
        targets,
        prior_titles=prior_titles,
    )

    feature_scores = {
        "lexical_nearest1_distance": {
            paper_id: value.nearest1_distance
            for paper_id, value in features.items()
        },
        "lexical_nearest3_distance": {
            paper_id: value.nearest3_distance
            for paper_id, value in features.items()
        },
        "lexical_oov_share": {
            paper_id: value.oov_token_share
            for paper_id, value in features.items()
        },
    }

    outcomes = _outcomes_from_cohort(cohort)
    if not outcomes:
        raise ValueError("cohort artifact has no supported outcome labels")

    k = int(cohort.get("review_budget_k", 5))
    matrix = evaluate_feature_outcome_matrix(
        feature_scores,
        outcomes=outcomes,
        k=k,
    )

    per_paper = {}
    for paper_id, value in features.items():
        per_paper[paper_id] = value.as_dict()

    known_tokens = sum(
        int(value.n_known_tokens) for value in features.values()
    )
    total_tokens = sum(
        int(value.n_tokens) for value in features.values()
    )

    return {
        "ablation": "historical title lexical novelty",
        "claim_boundary": (
            "Transparent lexical proxy only. It is not an embedding novelty "
            "measure, not a published atypical-combination metric, and not "
            "evidence of scientific importance."
        ),
        "target_cohort": {
            "filters": cohort["sampling"]["filters"],
            "seed": cohort["sampling"]["seed"],
            "sample_id_sha256": cohort["sampling"].get(
                "sample_id_sha256"
            ),
            "n": len(cases),
            "feature_cutoff_year": cohort["temporal_design"][
                "feature_cutoff_year"
            ],
            "outcome_endpoint_year": cohort["temporal_design"][
                "outcome_observation_end_year"
            ],
        },
        "prior_corpus": {
            "n_titles": len(prior_titles),
            "n_ids": len(prior_ids or []),
            "sample_id_sha256": (
                _hash_ids(list(prior_ids))
                if prior_ids
                else None
            ),
            "provenance": dict(prior_provenance or {}),
        },
        "coverage": {
            "target_title_count": len(targets),
            "total_target_tokens": total_tokens,
            "known_target_tokens": known_tokens,
            "known_token_share": (
                known_tokens / total_tokens
                if total_tokens
                else 0.0
            ),
        },
        "feature_direction": {
            "lexical_nearest1_distance": "higher = more lexically distant",
            "lexical_nearest3_distance": "higher = more lexically distant",
            "lexical_oov_share": "higher = more target tokens unseen in prior corpus",
        },
        "feature_outcome_matrix": matrix,
        "per_paper_features": per_paper,
    }


def run_live(
    cohort_path: str | Path,
    *,
    prior_filters: str,
    prior_sample_size: int,
    prior_seed: int,
    api_key: str | None = None,
) -> dict[str, Any]:
    """Sample a pre-target title corpus and evaluate lexical features."""
    cohort = json.loads(
        Path(cohort_path).read_text(encoding="utf-8")
    )
    prior = sample_works(
        filters=prior_filters,
        sample_size=prior_sample_size,
        seed=prior_seed,
        api_key=api_key,
    )
    titles = [work.title for work in prior]
    ids = [work.openalex_id for work in prior]
    return evaluate_lexical_ablation(
        cohort,
        prior_titles=titles,
        prior_ids=ids,
        prior_provenance={
            "source": "OpenAlex live API",
            "filters": prior_filters,
            "sample_size_requested": prior_sample_size,
            "sample_size_analyzed": len(prior),
            "seed": prior_seed,
            "temporal_rule": "prior corpus years strictly precede target cohort year",
            "field_assignment_temporality": (
                "current OpenAlex primary-topic field; exploratory stratification only"
            ),
        },
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cohort", required=True, type=Path)
    parser.add_argument("--prior-filters", required=True)
    parser.add_argument("--prior-sample-size", type=int, default=100)
    parser.add_argument("--prior-seed", type=int, required=True)
    parser.add_argument("--api-key", default=None)
    parser.add_argument("--output", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = run_live(
        args.cohort,
        prior_filters=args.prior_filters,
        prior_sample_size=args.prior_sample_size,
        prior_seed=args.prior_seed,
        api_key=args.api_key,
    )
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
