# ARIS4C012 · Agent takeover brief

## What this project is

**When Opposites Become Causes: An Indexed Cross-Domain Framework for Oppositional Causal Inversion**

A falsification-first attempt to define a restricted, cross-domain class of causal effects in which an exposure/intervention produces a **prespecified functional opposite** after explicit actor, level, time, construct, environment, feedback, or capacity distinctions are restored.

The project no longer claims to discover a general science of backfire. Existing unintended-consequence, paradox, rebound, complex-systems, boomerang, iatrogenic, Goodhart/proxy-failure, and related literatures already cover that broad territory.

## Current state

- **Stage:** Pilot 0B complete · v1 reliability revision gate
- **Activity:** at gate
- **Independent Coder B:** complete
- **Coder B commit:** `8f9ec0dd99e25ae0411fd4e06d2b4dbd1ef219d9`
- **Retrieval:** reproducible Pilot frame complete (165 candidates from 1,800 raw hits)
- **Raw reliability workflow:** `READY_FOR_ADJUDICATION`
- **Scientific reliability verdict:** v1 did **not** pass the prespecified reliability gate
- **Primary next task:** diagnose disagreement types, freeze Schema v2, run a fresh independent A2/B2 Pilot

## Key raw reliability

| Field | Raw agreement | Cohen's kappa | Krippendorff alpha |
|---|---:|---:|---:|
| opposition_valid | 0.767 | 0.466 | 0.463 |
| oci_candidate | 0.833 | 0.592 | 0.597 |
| primary_mechanism | 0.000 | 0.000 | -0.042 |

There are 141 disagreement cells.

The frozen workflow threshold says low opposition-validity or primary-mechanism reliability requires definition revision and a fresh sample before full screening.

## Critical interpretation

Do **not** read `primary_mechanism kappa = 0` as pure scientific disagreement.

The v1 instrument allowed incompatible vocabularies between coders, for example:

- `level-switch/interdependence` vs `level_switch`
- `strategic equilibrium feedback` vs `strategic_feedback`
- `meta-analysis` vs `meta_analysis`
- `support` vs `yes`

So Pilot 0B demonstrates a real **instrument/schema standardization failure** plus some genuine conceptual disagreements.

The raw reliability outputs must remain unchanged. Any normalization/adjudication is diagnostic and cannot retroactively turn v1 into a preregistered pass.

## Immediate next action

1. Read `process/PILOT0B_RELIABILITY_AUDIT.md`.
2. Diagnose the 141 disagreement cells into:
   - lexical/token mismatch;
   - overlapping schema categories;
   - genuine conceptual disagreement;
   - source/metadata disagreement.
3. Finalize/freeze `process/SCHEMA_V2_PROPOSAL.md` into a controlled-vocabulary v2.
4. Draw a fresh balanced validation sample.
5. Run independent A2/B2 coding.
6. Only after v2 passes reliability, proceed to full 165-record screening.

## Canonical files / entry points

- `process/STATUS.md` — canonical current scientific state
- `process/PILOT0B_RELIABILITY_AUDIT.md` — current reliability interpretation
- `process/SCHEMA_V2_PROPOSAL.md` — leading redesign
- `data/pilot0_coderB_blind.csv` — completed independent B
- `data/reliability/pilot0_reliability_summary.json` — immutable raw reliability
- `data/reliability/pilot0_disagreements.csv` — raw disagreement packet
- `process/RETRIEVAL_FRAME_AUDIT.md` — 165-record frame structure
- `manuscript/DRAFT.md` — current manuscript draft
- `manuscript/REFERENCES.md` — working bibliography

## Locked decisions

- Functional opposition must be prespecified.
- OCI candidacy and empirical support are separate.
- No grand pooled OCI effect size.
- Raw retrieval frequency is not prevalence.
- Orwell's slogans are motivating stress tests, not literal scientific conclusions.
- The broad novelty claim has failed; only a validated indexed representation remains potentially novel.
- Do not reuse Pilot 0 as the sole validation set for v2.

## Handoff completion rule

Before ending a substantial future session:
- update `process/STATUS.md`;
- update `TODO.md`;
- append material decisions to `DECISIONS.md`;
- append a public-safe conversation summary to `CHATLOG.md`;
- append executed/validated work to `SESSION_LOG.md`.
