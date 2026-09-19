# ARIS4C009 · Status

**Current stage:** empirical Pilot-0 / rater-gated  
**ARIS baseline:** v0.4.26  
**Canonical scope:** quantify acquisition and encoding divergence separately before mechanistic expansion.

## Completed

- [x] Canonical research question defined.
- [x] Source evidence distinguished from latent lived-state ground truth.
- [x] Acquisition (A_m) and encoding (E_k) formally separated.
- [x] 009A split into 009A1 same-source encoding benchmark and 009A2 acquisition benchmark.
- [x] Actual self-report separated from questionnaire-format source projection.
- [x] Intended-use validity separated from source-reconstruction fidelity.
- [x] Use-conditioned Pareto frontier specified.
- [x] Rate-distortion formulation restricted to fixed-source encoding.
- [x] Independent fidelity metrics, relation ontology and query bank specified.
- [x] Power/precision sensitivity framework added.
- [x] Adversarial audit completed and fatal-design confounds corrected.
- [x] Expanded Gate A novelty review completed; broad novelty claims retired.
- [x] 009A1 preregistration-ready protocol skeleton revised.
- [x] 009A2 acquisition protocol drafted.
- [x] Physical-context constraint layer specified separately.
- [x] DAIS-C selected as open real-clinical Pilot-0 engineering corpus.
- [x] Official DAIS-C archive downloaded successfully in GitHub Actions.
- [x] Raw psychiatric transcript publication blocked by an allowlist privacy gate.
- [x] Archive SHA-256 and aggregate structural inventory recorded.
- [x] TXT/RTF/DOCX transcript representations structurally classified.
- [x] 28 unique full-interaction transcript files recovered in the public archive layer.
- [x] Full-interaction participant-word scale cross-checked against speaker-only representation.
- [x] Privacy-preserving candidate-episode parser implemented.

## Gate A — novelty

**Status:** conditional pass for research development.

The defensible candidate contribution is the integrated acquisition/encoding benchmark architecture, not any single component.

Formal manuscript-stage multi-database screening remains required.

## Gate B — 009A1 source engineering

**Status:** passed for Pilot-0 engineering.

DAIS-C is adequate for:

- parser testing;
- source provenance;
- episode-boundary calibration;
- query-bank feasibility;
- relation-graph feasibility;
- R3P/R4P projection feasibility;
- evaluator-blinding workflow.

DAIS-C is **not** treated as an EASE/EAWE/STEP corpus.

## Gate C — episode-boundary validation

**Status:** next blocker.

The machine parser defines a candidate episode as:

> one interviewer block + all immediately following participant blocks until the next interviewer block.

Before semantic fidelity scoring:

1. sample calibration episodes;
2. two trained raters judge split/merge/reject;
3. quantify boundary agreement/error;
4. revise if needed;
5. freeze parser rule.

## Gate D — source/query/relation calibration

After episode boundaries are frozen, estimate:

- source answerability;
- query redundancy;
- adjudication agreement;
- relation-annotation reliability;
- usable query yield;
- evaluator variance;
- R3P/R4P projection feasibility.

## Gate E — 009A1 confirmatory representation benchmark

Minimum conditions:

- R0 rich source;
- R1 episode graph;
- R2 phenomenology-informed structured code;
- R3P questionnaire-format projection;
- R4P conventional symptom-code projection.

For DAIS-C, R2 is explicitly **R2-lite**, not an EASE score.

## Gate F — richer psychosis Pilot-1

**Preferred target:** AMP-SCZ under approved NIMH Data Archive access.

Rationale:

- PSYCHS;
- open-ended interview language samples;
- transcript-level psychosis-risk material;
- multimodal clinical/contextual data.

Pilot-1 is where direct psychosis-risk measurement claims should be tested.

## Gate G — 009A2 acquisition pilot

Purpose-collected randomized matched-content acquisition study remains separate and requires ethics/data collection.

## Gate H — multimodal/mechanistic extension

Deferred until measurement layers survive.

## Current blocker

The project now has real Pilot-0 data.

The next high-value input is **independent human boundary/adjudication work**, not more conceptual expansion.

## Scope control

009A1 = encoding measurement.  
009A2 = acquisition measurement.  
009B = cross-level mechanism.  
009C = longitudinal idiographic dynamics.  
009D = perturbation/intervention validation.
