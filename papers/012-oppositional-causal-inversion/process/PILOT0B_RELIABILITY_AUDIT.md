# PILOT 0B RELIABILITY AUDIT — ARIS4C012

Updated: 2026-09-19

## Executive verdict

**Independent Coder B: COMPLETE and provenance-preserved.**  
**Raw v1 reliability gate: NOT PASSED.**  
**Interpretation: schema/instrument revision is required before full evidence-map screening.**

The reliability workflow reports `READY_FOR_ADJUDICATION`, which means the two coder files are complete and mechanically comparable. It does **not** mean the prespecified scientific reliability gate passed.

## Independent Coder B provenance

Coder B was completed by an isolated WorkBuddy run and committed as:

- commit: `8f9ec0dd99e25ae0411fd4e06d2b4dbd1ef219d9`
- message: `ARIS4C012: independent blind Coder B complete`
- coded file: `data/pilot0_coderB_blind.csv`
- current coded-file blob: `d7de922fd2227d63e9ec66883b127fe185d8becd`

The commit records that all P01–P30 core fields were completed, no Coder A material was opened, and the frozen v1 inputs were re-verified against `CODER_B_FREEZE.json`.

The blank pre-coding packet remains preserved in Git history at blob:

`22baa1d0bd65e42e1b12e15dba11d67487709cf7`

## Raw reliability results

Source: `data/reliability/pilot0_reliability_summary.json`

| Field | n | Raw agreement | Cohen's kappa | Krippendorff alpha |
|---|---:|---:|---:|---:|
| opposition_valid | 30 | 0.767 | 0.466 | 0.463 |
| oci_candidate | 30 | 0.833 | 0.592 | 0.597 |
| primary_mechanism | 30 | 0.000 | 0.000 | -0.042 |
| evidence_mode | 30 | 0.600 | 0.522 | 0.519 |
| evidence_tier | 30 | 0.267 | 0.223 | 0.179 |
| causal_claim_strength | 30 | 0.000 | 0.000 | -0.083 |
| result_support | 30 | 0.033 | 0.022 | -0.065 |

Total disagreement cells: **141**.

The frozen workflow rule stated that opposition-validity or primary-mechanism agreement below 0.70 requires definition revision and a fresh sample before full screening. Therefore v1 does **not** pass the reliability gate.

## Critical measurement problem discovered

The zero or near-zero agreement in several fields cannot be interpreted as pure substantive disagreement because Coder A and Coder B often used different value vocabularies.

Examples from the frozen disagreement packet:

- `level-switch/interdependence` vs `level_switch`
- `strategic equilibrium feedback` vs `strategic_feedback`
- `choice overload` vs `capacity_overload`
- `meta-analysis` vs `meta_analysis`
- `support` vs `yes`
- free-text causal-strength descriptions vs the B-side ordinal tokens `strong/moderate/weak/none`

The scorer correctly performed literal nominal comparison, but the coding instrument did not force both coders onto one canonical controlled vocabulary. Therefore:

1. the raw reliability output must remain preserved;
2. it must **not** be cosmetically overwritten by post-hoc synonym normalization;
3. mechanism kappa = 0 must not be described as proof that the underlying scientific concepts are completely unrelated;
4. the Pilot demonstrates a real **instrument/schema failure**: the v1 fields were insufficiently standardized for independent nominal reliability.

## Genuine substantive disagreements still exist

Not all disagreement is lexical. Examples requiring source-level adjudication include:

- P03 deterrence: OCI candidate yes vs no;
- P13 information avoidance: opposition validity / OCI candidacy disagreement;
- P30 counterfinality: opposition validity / OCI candidacy disagreement;
- several uncertainty vs yes/no distinctions;
- disagreements about whether neighboring theories count as strict functional-opposite cases.

These are scientifically informative and should be retained as diagnostic cases.

## Consequence for Schema v2

The pre-existing `SCHEMA_V2_PROPOSAL.md` was drafted before seeing Coder B labels and is now strongly motivated by the observed v1 failure mode.

Its key correction is to separate:

- **opposition relation**;
- **index-switch vector** (actor / level / time / construct / environment);
- **generative-mechanism vector**;
- **evidence mode / strength**;
- **result direction**.

This avoids forcing coders to choose one `primary_mechanism` when multiple index switches and mechanisms can simultaneously be true.

## Next scientific steps

1. Keep the raw v1 reliability summary and disagreement packet immutable.
2. Adjudicate disagreements **for diagnosis**, explicitly distinguishing:
   - lexical/token-vocabulary mismatch;
   - schema-category overlap;
   - genuine conceptual disagreement;
   - source/metadata disagreement.
3. Freeze a revised v2 controlled vocabulary and coding form.
4. Draw a **fresh balanced sample**; do not reuse Pilot 0 as the sole validation set.
5. Run genuinely independent A2/B2 coding under v2.
6. Recompute reliability using identical allowed categorical values for both coders.
7. Only after the revised schema passes the reliability gate should the 165-record evidence-map frame be fully screened.

## Claim discipline

The current evidence supports saying:

> The Pilot shows that the broad OCI idea is codeable enough to produce substantial raw agreement on candidacy, but the v1 coding instrument is not sufficiently reliable or standardized for a validated cross-domain taxonomy.

It does **not** yet support saying:

- OCI is a validated general framework;
- the eight v1 mechanism classes are reliable;
- the prevalence of OCI families is known;
- full evidence-map screening can proceed without schema revision.

## Recovery note

If a future chat/agent resumes this project, read in this order:

1. `handoff/AGENT_HANDOFF.md`
2. `process/PILOT0B_RELIABILITY_AUDIT.md`
3. `process/SCHEMA_V2_PROPOSAL.md`
4. `data/reliability/pilot0_reliability_summary.json`
5. `data/reliability/pilot0_disagreements.csv`
6. `process/STATUS.md`

