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
