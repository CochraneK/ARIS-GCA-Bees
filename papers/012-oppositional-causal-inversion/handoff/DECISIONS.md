# ARIS4C012 · Decision log

This file is append-oriented. Preserve superseded decisions when they explain why the project changed direction; mark them as superseded rather than deleting them.

## 2026-09-19 · Continuity-standard bootstrap

**Decision:** Adopt the repository-level ARIS4C continuity/handoff contract for this paper.

**Why:** The project must remain recoverable across ChatGPT conversations, accounts, computers, and external agents without relying on one chat's memory.

**Project-specific decisions distilled from surviving project context:**
- Restrict the construct to functional-opposite-producing causal effects.
- Independent construct coding is a hard gate before broad claims.

**Canonical follow-up:** Future material decisions should be appended with date, rationale, and affected files/commits when known.

## 2026-09-19 · Broad novelty claim rejected

**Decision:** Do not present OCI as a newly discovered general science of unintended consequences/backfire.

**Why:** Prior-art saturation found mature umbrella frameworks spanning Merton/Boudon unintended consequences, complex adaptive-system feedback, paradox theory, rebound/Jevons, Braess, boomerang/iatrogenic effects, psychological reactance, safe-development effects, and Goodhart/proxy failure.

**Remaining provisional novelty:** the combination of:
1. prespecified functional opposition;
2. explicit index restoration;
3. independently validated cross-domain coding.

**Affected files:** `process/NOVELTY_AUDIT.md`, `process/PRIOR_ART_SATURATION.md`, `manuscript/DRAFT.md`.

## 2026-09-19 · Pilot 0B is complete, but v1 reliability did not pass

**Decision:** Treat WorkBuddy Pilot 0B as genuinely independent and complete, but do **not** promote v1 as a validated taxonomy.

**Evidence:**
- Coder B commit: `8f9ec0dd99e25ae0411fd4e06d2b4dbd1ef219d9`
- opposition_valid kappa = 0.466
- oci_candidate kappa = 0.592
- primary_mechanism kappa = 0.000
- 141 disagreement cells

**Why:** The frozen workflow required revision and a fresh sample if opposition-validity or primary-mechanism agreement was below 0.70.

## 2026-09-19 · Raw reliability must remain immutable

**Decision:** Do not post-hoc synonym-normalize the raw v1 reliability file and then report the revised number as if it were preregistered reliability.

**Why:** Several disagreements are clearly token/vocabulary mismatches (for example `meta-analysis` vs `meta_analysis`, or `strategic equilibrium feedback` vs `strategic_feedback`), while others are genuine conceptual disagreements. These must be diagnosed separately.

**Consequence:** The raw summary is preserved as an instrument-validation result. Any normalization/adjudication is diagnostic only.

## 2026-09-19 · Schema v2 becomes the leading redesign

**Decision:** Use `process/SCHEMA_V2_PROPOSAL.md` as the basis for the next coding instrument, subject to explicit freeze before a new Pilot.

**Why:** v1 mixed index switches with generative mechanisms in a forced single `primary_mechanism` field. v2 separates:
- opposition relation;
- index-switch vector;
- mechanism vector;
- evidence mode/strength;
- result direction.

**Safeguard:** Do not retroactively recode Pilot 0 and call it v2 validation. Draw a fresh balanced sample and run independent A2/B2 coding.

## 2026-09-19 · Evidence-map screening remains gated

**Decision:** Do not begin full 165-record scientific screening as though the taxonomy were validated.

**Why:** Retrieval is reproducible, but construct reliability is not yet sufficient.

**Next gate:** diagnostic adjudication -> frozen controlled-vocabulary v2 -> fresh independent A2/B2 reliability Pilot.

## 2026-09-19 · Exhaustive v1 disagreement diagnosis completed

**Decision:** Treat the 141-cell Pilot 0B diagnosis as a failure-mode partition, not as post-hoc adjudication or a replacement reliability analysis.

**Result:** 30 lexical/token-vocabulary mismatches; 24 schema-category overlaps; 26 source/metadata disagreements; 61 genuine conceptual disagreements.

**Why:** This preserves the frozen raw v1 reliability result while separating instrument-design failure from disagreements that still require source-level or conceptual review. The 24 mechanism schema-overlap cells strengthen the rationale for orthogonal Schema v2 axes, but the 61 genuine conceptual cells show that string normalization alone cannot solve reliability.

**Canonical artifacts:** `data/reliability/pilot0_disagreement_diagnosis.csv`, `data/reliability/pilot0_disagreement_diagnosis_summary.json`, `process/PILOT0B_DISAGREEMENT_DIAGNOSIS.md`, `code/diagnose_pilot0_disagreements.py`.

**Next gate:** freeze controlled-vocabulary Schema v2, then draw a fresh balanced validation sample for independent A2/B2 coding.

## 2026-09-19 · Controlled-vocabulary Schema v2 frozen

**Decision:** Freeze v2 as an orthogonal coding instrument for a fresh independent A2/B2 validation sample; do not use it to retroactively recode Pilot 0B.

**Structure:** entry gate; five opposition-relation indicators; five index-switch indicators; eight generative-mechanism indicators; ten evidence-mode indicators; controlled evidence strength; controlled result direction; controlled normative valence. Multi-label axes are binary/uncertain rather than forced single categories.

**Reliability gate:** opposition-valid κ >= 0.70; informative secondary axes require κ >= 0.60 and raw agreement >= 0.80, with median informative-axis κ >= 0.70. Undefined κ from degenerate sparse axes is reported rather than treated as a pass.

**Canonical artifacts:** `process/SCHEMA_V2_FROZEN.md`, `process/SCHEMA_V2_FREEZE.json`, `data/v2_validation_coding_template.csv`.

**Next gate:** draw a fresh balanced sample and freeze blind A2/B2 packets before any new reliability scoring.

## 2026-09-19 · Fresh v2 validation sample frozen

**Decision:** Freeze a fresh 30-record validation sample from the 165-record reproducible frame using a deterministic fixed-seed draw, after excluding all Pilot 0B records by stable identifier/title.

**Design:** 6 retrieval strata × 5 records each; fixed seed `ARIS4C012-V2-A2B2-20260919`; FNV-1a 32-bit score over seed + dedupe key; ascending score within stratum; zero overlap with Pilot 0B. Provider mix is 14 OpenAlex / 16 Crossref.

**Why:** v2 requires fresh validation rather than retroactive recoding. The frozen sample is balanced across the existing retrieval strata while remaining reproducible.

**Boundary:** the manifest is not yet a coder packet. Identical blinded evidence packets must be materialized and hashed before independent A2/B2 coding.

**Canonical artifacts:** `data/v2_validation_sample_manifest.csv`, `process/V2_VALIDATION_SAMPLE_FREEZE.json`, `process/V2_VALIDATION_SAMPLE_AUDIT.md`, `code/draw_v2_validation_sample.py`.
