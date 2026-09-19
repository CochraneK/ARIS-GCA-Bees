# ARIS4C009 · Status

**Current stage:** empirical Pilot-0 / human-boundary-calibration gate  
**ARIS baseline:** v0.4.26  
**Canonical scope:** quantify acquisition and encoding divergence separately before mechanistic expansion.

## Completed

- [x] Acquisition and encoding formally separated.
- [x] 009A1 fixed-source encoding benchmark specified.
- [x] 009A2 acquisition-method benchmark specified separately.
- [x] Fidelity separated from reliability, intended-use validity, prediction and burden.
- [x] Independent query/adjudication/evaluation architecture specified.
- [x] Relation ontology, data dictionary and power/precision framework drafted.
- [x] Adversarial audit completed.
- [x] Expanded Gate A novelty audit completed; broad priority claims retired.
- [x] DAIS-C selected as open real-clinical Pilot-0 engineering corpus.
- [x] Official archive automatically downloaded from UK Data Service.
- [x] Archive checksum and privacy-preserving inventory published.
- [x] Raw psychiatric transcript publication blocked by workflow allowlist.
- [x] TXT/RTF/DOCX representations structurally classified.
- [x] 28 public full-interaction transcripts recovered: 15 clinical-source, 13 comparison-source.
- [x] Microepisode parser run on real data.
- [x] 1,908 interviewer-anchored candidate microepisodes inventoried.
- [x] Microepisode rule rejected as too granular for direct fidelity scoring.
- [x] 20/40/80-word multi-turn segmentation sensitivity completed.
- [x] 20- and 40-word strategies advanced to blinded human calibration.
- [x] 80-word strategy deferred because it combines more microepisodes and increases long-window burden.
- [x] Private local packet generator implemented.
- [x] Aggregate boundary-rating scorer implemented.
- [x] DAIS-C no-disease-inference limitations frozen.

## Current empirical facts from Pilot-0

### Full interaction layer

- 28 usable full-interaction transcripts in the public archive layer.
- participant-word count in full interaction ≈ speaker-only representation, supporting source recovery.
- raw texts remain outside Git.

### Microepisodes

- 1,908 interviewer-anchored units;
- 1,871 include participant response;
- participant words: median 14, IQR 2–50.

Conclusion: one-question/one-response units are too often trivial.

### Segmentation sensitivity

- target 20 → 953 windows; median 52 participant words; median 1 microepisode/window;
- target 40 → 745 windows; median 79 words; median 2 microepisodes/window;
- target 80 → 550 windows; median 116 words; median 3 microepisodes/window.

No strategy is canonical until human calibration.

## Gate A — novelty

**Conditional pass for research development.**

Formal manuscript-stage database screening remains required.

## Gate B — source engineering

**Passed for DAIS-C Pilot-0.**

The pipeline can reproducibly retrieve, classify and structurally segment real
schizophrenia interview material without publishing raw text.

## Gate C — human boundary calibration

**Current blocker.**

Need two independent raters to complete the blinded 20-vs-40 boundary packet.

Primary outputs:

- coherence;
- sufficiency for nontrivial query construction;
- mixed-topic rate;
- keep/merge/split/reject;
- Gwet AC1.

## Gate D — query / relation calibration

After boundary rule is frozen:

- build source-only queries;
- estimate answerability;
- remove redundant queries;
- calibrate relation annotation;
- estimate evaluator variance;
- test R3P/R4P projection feasibility.

## Gate E — 009A1 representation benchmark

Minimum representations:

- R0 source;
- R1 relation graph;
- R2-lite phenomenology-informed structure for DAIS-C;
- R3P questionnaire-format projection;
- R4P conventional symptom-style projection.

DAIS-C is not an EASE corpus.

## Gate F — richer psychosis Pilot-1

Preferred target: AMP-SCZ under approved NIMH Data Archive access.

This is the stronger substrate for PSYCHS/open-interview and later multimodal validation.

## Gate G — 009A2 acquisition study

Requires purpose-collected human data and ethics approval.

## Current blocker

The next irreducible input is **two independent human raters**.

More automated conceptual expansion before this gate has lower value than completing the calibration.

## Scope control

009A1 = encoding measurement.  
009A2 = acquisition measurement.  
009B = cross-level mechanism.  
009C = longitudinal idiographic dynamics.  
009D = perturbation/intervention validation.
