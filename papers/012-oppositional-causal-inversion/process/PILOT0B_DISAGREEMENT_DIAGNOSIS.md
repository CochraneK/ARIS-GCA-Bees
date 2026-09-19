# PILOT 0B disagreement diagnosis — ARIS4C012

Updated: 2026-09-19

## Status

The **141 raw v1 disagreement cells remain unchanged**. This artifact diagnoses likely failure modes only; it does not alter either coder's labels, fill `adjudicated_value`, or recompute a cosmetically improved reliability statistic.

## Exhaustive diagnostic partition

| Diagnosis | Cells | Interpretation |
|---|---:|---|
| lexical/token-vocabulary mismatch | 30 | Different separators, free-text vs ordinal tokens, or evidence/result label granularity that can be cross-walked without claiming scientific agreement |
| schema-category overlap | 24 | Primarily `primary_mechanism`: v1 forces index switches / free-text mechanisms against a different controlled mechanism family |
| source/metadata disagreement | 26 | Evidence-mode or evidence-tier classification requires explicit source-level crosswalk/review |
| genuine conceptual disagreement | 61 | Opposition, candidacy, index-switch, mechanism-none, causal-strength, or result-direction judgments still differ after coarse lexical normalization |

Total: **141 / 141 cells classified**.

## Field-level findings

- `primary_mechanism`: 24 schema-overlap cells + 6 genuine conceptual cells.
- `evidence_mode`: 8 lexical/granularity cells + 4 source/metadata cells.
- `evidence_tier`: 22 source/metadata cells.
- `causal_claim_strength`: 6 lexical/ordinal-crosswalk cells + 24 genuine conceptual cells.
- `result_support`: 16 lexical/coarse-token cells + 13 genuine conceptual cells.
- Entry/index judgments contribute the remaining genuine conceptual disagreements: `opposition_valid` 7, `oci_candidate` 5, `actor_switch` 1, `nonlinearity` 2, `selection_filtering` 1, `feedback` 1, `time_switch` 1.

## Scientific implication

The diagnostic supports the pre-existing Schema v2 direction without retroactively validating it. In particular, the 24 schema-overlap mechanism cells show why a forced single `primary_mechanism` nominal label is a poor reliability target when an index switch and one or more generative mechanisms can simultaneously be true.

At the same time, **61 cells remain genuinely conceptual** under this coarse diagnostic. Schema redesign therefore cannot be treated as merely a string-normalization exercise.

## Next gate

1. Preserve raw Pilot 0B files and statistics.
2. Use this diagnosis to freeze one controlled vocabulary for Schema v2.
3. Specify per-axis allowed values and missing/uncertain rules.
4. Draw a **fresh** balanced validation sample.
5. Run genuinely independent A2/B2 coding and score reliability per orthogonal axis.
6. Keep full 165-record evidence-map screening gated until the revised instrument passes.

## Reproducibility

- Raw input: `data/reliability/pilot0_disagreements.csv`
- Diagnostic output: `data/reliability/pilot0_disagreement_diagnosis.csv`
- Machine-readable summary: `data/reliability/pilot0_disagreement_diagnosis_summary.json`
- Reproducer: `code/diagnose_pilot0_disagreements.py`

The diagnostic categories are **failure-mode labels**, not adjudicated scientific truth.
