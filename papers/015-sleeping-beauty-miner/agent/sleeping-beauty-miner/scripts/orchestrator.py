"""Reference orchestrator for ARIS4C015 Sleeping Beauty Miner.

Input is JSON on stdin; output is one Candidate Evidence Card JSON object.

This reference orchestrator intentionally avoids claiming a validated
prospective model. It handles deterministic trajectory reconstruction,
cutoff-safe baselines, retrospective metrics, and ARIS4C011 routing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve()
CODE_DIR = HERE.parents[3] / "code"
if str(CODE_DIR) not in sys.path:
    sys.path.insert(0, str(CODE_DIR))

from baselines import baseline_score, cutoff_features  # noqa: E402
from candidate_card import build_candidate_card, evidence_item  # noqa: E402
from citation_history import (  # noqa: E402
    CitationHistory,
    citation_history_from_citing_years,
    truncate_history,
)
from integrity_adapter import adapt_011_findings  # noqa: E402
from sb_metrics import retrospective_summary  # noqa: E402


def _history_from_request(request: dict[str, Any]) -> CitationHistory:
    publication_year = int(request["publication_year"])

    if "citation_history" in request:
        counts = tuple(int(x) for x in request["citation_history"])
        if not counts:
            raise ValueError("citation_history must be non-empty")
        end_year = publication_year + len(counts) - 1
        return CitationHistory(
            publication_year=publication_year,
            end_year=end_year,
            counts=counts,
            valid_edges=sum(counts),
            invalid_prepublication_edges=0,
        )

    if "citing_years" in request:
        return citation_history_from_citing_years(
            publication_year,
            request["citing_years"],
            end_year=request.get("observation_end_year"),
            strict=False,
        )

    raise ValueError(
        "Provide either citation_history or citing_years to the reference orchestrator"
    )


def run(request: dict[str, Any]) -> dict[str, Any]:
    mode = str(request.get("mode", "PROSPECTIVE")).upper()
    if mode not in {"RETROSPECTIVE", "PROSPECTIVE", "DISCOVERY_SCAN"}:
        raise ValueError(f"Unsupported mode: {mode}")

    paper_id = str(request["paper_id"])
    full_history = _history_from_request(request)
    cutoff = request.get("cutoff_year")

    visible_history = full_history
    if mode in {"PROSPECTIVE", "DISCOVERY_SCAN"}:
        if cutoff is None:
            raise ValueError("Prospective modes require cutoff_year")
        visible_history = truncate_history(full_history, int(cutoff))

    integrity_gate = adapt_011_findings(
        request.get("integrity_findings", []),
        cutoff_year=int(cutoff) if cutoff is not None and mode != "RETROSPECTIVE" else None,
    )

    evidence: list[dict[str, Any]] = []
    feature_values = cutoff_features(visible_history.counts)
    evidence.append(
        evidence_item(
            name="citation_trajectory",
            applicable=True,
            cutoff_safe=True,
            status="NEUTRAL",
            value=feature_values.as_dict(),
            provenance=list(request.get("provenance", ["request"])),
            notes=(
                "Trajectory features are descriptive. They do not establish "
                "future impact or scientific validity."
            ),
        )
    )

    for supplied in request.get("evidence_families", []):
        evidence.append(
            evidence_item(
                name=str(supplied["name"]),
                applicable=bool(supplied.get("applicable", True)),
                cutoff_safe=bool(supplied.get("cutoff_safe", False)),
                status=str(supplied.get("status", "ABSTAIN")),
                value=supplied.get("value"),
                provenance=supplied.get("provenance", []),
                uncertainty=supplied.get("uncertainty"),
                notes=supplied.get("notes"),
            )
        )

    retrospective = {}
    if mode == "RETROSPECTIVE":
        retrospective = retrospective_summary(full_history.counts)

    strategy = request.get("baseline_strategy")
    score = None
    score_semantics = None
    if strategy:
        score = baseline_score(feature_values, str(strategy))
        score_semantics = (
            f"Transparent baseline '{strategy}' computed using only the "
            "visible citation trajectory. Not a validated awakening probability."
        )

    requested_state = str(
        request.get("candidate_state", "INSUFFICIENT_DATA")
    ).upper()

    explanation = request.get("explanation")
    if explanation is None:
        explanation = (
            "Reference orchestrator completed deterministic evidence assembly. "
            "No validated prospective classifier is implied."
        )

    return build_candidate_card(
        paper_id=paper_id,
        identifiers=request.get("identifiers"),
        mode=mode,
        analysis_cutoff=(
            int(cutoff)
            if cutoff is not None
            else int(full_history.end_year)
        ),
        state=requested_state,
        evidence_families=evidence,
        integrity_gate=integrity_gate,
        provenance=request.get("provenance", ["request"]),
        citation_trajectory=visible_history.as_dict(),
        retrospective_metrics=retrospective,
        prince_candidates=request.get("prince_candidates", []),
        rank=request.get("rank"),
        score=score,
        score_semantics=score_semantics,
        explanation=str(explanation),
        model_version=request.get("model_version", "deterministic-reference-0.1"),
    )


def main() -> None:
    payload = json.load(sys.stdin)
    result = run(payload)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
