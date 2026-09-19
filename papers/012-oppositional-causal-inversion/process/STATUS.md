# STATUS — ARIS4C012

Updated: 2026-09-19

## State

**PILOT 0B COMPLETE · RAW V1 RELIABILITY GATE NOT PASSED · SCHEMA REVISION / FRESH PILOT REQUIRED**

## Canonical identity

**When Opposites Become Causes: An Indexed Cross-Domain Framework for Oppositional Causal Inversion**

ARIS4C012 does not attempt to prove Orwell's slogans literally true. It tests whether superficially contradictory causal claims can be decomposed into a prespecified functional-opposition relation plus explicit actor, level, time, construct, environment, feedback, and capacity distinctions.

## Current evidence state

### Concept / prior art
- literal `X = not-X` framing rejected;
- indexed construct representation defined as `X[a,l,t,d,e]`;
- functional-opposition validity rules defined;
- broad novelty claim rejected after prior-art saturation;
- defensible novelty narrowed to:
  - prespecified functional opposition;
  - explicit index restoration;
  - independently validated cross-domain coding.

### Retrieval
- retrieval v0.1 preserved as a failed-but-informative semantic-contamination snapshot;
- retrieval v0.2 passed executable/provenance-safe and gross topical-relevance gates;
- 1,800 raw OpenAlex/Crossref hits;
- 1,375 transparent pre-screen rejections;
- 165 selected reproducible Pilot candidates;
- full systematic-review saturation/recall remains open;
- retrieval-frame audit shows query-family imbalance, so raw retrieval counts must not be treated as prevalence.

### Pilot 0A
Coder A feasibility labels:
- OCI candidate: 21 yes / 7 no / 2 uncertain;
- functional opposition: 21 yes / 4 no / 5 uncertain.

These are not prevalence estimates.

### Pilot 0B
A genuinely independent WorkBuddy Coder B completed all P01–P30 and committed the coded packet:

`8f9ec0dd99e25ae0411fd4e06d2b4dbd1ef219d9`

The commit documents that forbidden Coder A materials were not opened and that frozen v1 inputs were verified before coding.

Current coded B blob:

`d7de922fd2227d63e9ec66883b127fe185d8becd`

## Raw reliability result

The automated scorer reports `READY_FOR_ADJUDICATION`, meaning the coding files are complete. This is **not** a scientific Gate B pass.

Key raw metrics:

| Field | Raw agreement | Cohen's kappa | Krippendorff alpha |
|---|---:|---:|---:|
| opposition_valid | 0.767 | 0.466 | 0.463 |
| oci_candidate | 0.833 | 0.592 | 0.597 |
| primary_mechanism | 0.000 | 0.000 | -0.042 |

There are **141 disagreement cells** in the full packet.

The frozen workflow rule requires revision and a fresh sample if opposition-validity or primary-mechanism agreement is below 0.70. Therefore **v1 has not passed the reliability gate**.

See:

`process/PILOT0B_RELIABILITY_AUDIT.md`

## Important reliability interpretation

Several low-agreement fields suffer from a coding-instrument vocabulary mismatch rather than purely substantive disagreement.

Examples:
- `level-switch/interdependence` vs `level_switch`;
- `strategic equilibrium feedback` vs `strategic_feedback`;
- `meta-analysis` vs `meta_analysis`;
- `support` vs `yes`;
- free-text causal-strength labels vs ordinal controlled tokens.

The raw scorer should remain immutable. Do not post-hoc overwrite the raw kappa values with synonym-normalized values and call that preregistered reliability.

At the same time, do not interpret `primary_mechanism kappa = 0` as direct proof that the scientific mechanisms have zero conceptual agreement. The Pilot exposed a real **schema/instrument standardization failure**.

## Schema v2 status

A post-Gate-B `SCHEMA_V2_PROPOSAL.md` was drafted **before Coder B labels were inspected**.

It separates:
1. opposition relation;
2. index-switch vector;
3. generative-mechanism vector;
4. evidence mode / strength;
5. result direction.

This is now the leading redesign because v1 mixed index dimensions (actor/level/time/construct) with mechanisms (feedback/overload/filtering/power) in one forced `primary_mechanism` field.

Do not retroactively relabel Pilot 0 as a successful v2 validation.

## Novelty status

**BROAD CLAIM FAILED · NARROW INDEXED-REPRESENTATION CLAIM REMAINS PROVISIONAL.**

Major prior-art competitors include:
- Merton/Boudon unintended/perverse consequences;
- paradox theory;
- complex adaptive-system intervention backfire;
- boomerang and iatrogenic effects;
- rebound/Jevons effects;
- Braess paradox;
- safe-development effects;
- psychological reactance;
- ecological rationality / less-is-more;
- rational inattention / deliberate ignorance;
- Goodhart/Campbell proxy failure.

The possible contribution is a validated representation layer for a restricted class of functional-opposite-producing causal effects, not a new discovery that interventions sometimes backfire.

## Locked safeguards

- Functional opposites must be prespecified, not invented after seeing results.
- OCI candidacy and empirical support are separate.
- Null/counterevidence stays in the evidence map.
- No grand pooled OCI effect size.
- Raw retrieval frequency is not phenomenon prevalence.
- War/threat/competition/deterrence/cohesion/regime support/peace remain distinct constructs.
- Formal choice and effective autonomy remain distinct.
- Selective filtering and externally imposed ignorance remain distinct.
- Political cases are descriptive causal research objects, not advocacy.
- Coder B v1 provenance and raw reliability outputs must remain preserved.
- Any revised schema must be validated on a fresh independent sample.

## Current hard gate

### Gate B — construct reliability
**Independent coding: COMPLETE.**  
**Raw v1 reliability: FAILS prespecified threshold.**  
**Next action: diagnostic adjudication + schema revision + fresh A2/B2 Pilot.**

Adjudication should classify disagreements into:
- lexical/token mismatch;
- overlapping schema categories;
- genuine conceptual disagreement;
- source/metadata disagreement.

It must not be used to cosmetically convert v1 into a passed reliability test.

### Gate R — reproducible retrieval
- R1 executable/provenance-safe retrieval: **PASS**
- R2 gross topical relevance for Pilot retrieval: **PASS**
- R3 systematic-review saturation/recall: **OPEN**

## Next execution queue

1. Preserve the raw v1 reliability summary/disagreement packet unchanged.
2. Diagnose/adjudicate the 141 disagreement cells by disagreement type.
3. Finalize and freeze a controlled-vocabulary Schema v2.
4. Draw a fresh balanced validation sample.
5. Run genuinely independent A2/B2 coding under v2.
6. Recompute agreement with identical categorical vocabularies.
7. Only after revised reliability passes, screen the 165-record frame.
8. Target-expand underrepresented query families and perform backward/forward citation chasing.
9. Update manuscript results and limitations.
10. Produce final English paper + Chinese paper + evidence-traceable figures/tables under the ARIS4C output standard.

## Manuscript / support files already present

- `manuscript/DRAFT.md`
- `manuscript/REFERENCES.md`
- `process/NOVELTY_AUDIT.md`
- `process/PRIOR_ART_SATURATION.md`
- `process/RETRIEVAL_V0_1_AUDIT.md`
- `process/RETRIEVAL_V0_2_AUDIT.md`
- `process/RETRIEVAL_FRAME_AUDIT.md`
- `process/INTERNAL_REVIEW.md`
- `process/SCHEMA_V2_PROPOSAL.md`
- `process/PILOT0B_RELIABILITY_AUDIT.md`

## Handoff sentence

If the original chat is deleted, resume from `handoff/AGENT_HANDOFF.md` and this file. **ARIS4C012 has a complete independent Coder B and reproducible retrieval frame, but v1 did not pass the prespecified reliability gate. The next scientific task is diagnostic adjudication and a fresh v2 validation Pilot—not full evidence-map screening yet.**
