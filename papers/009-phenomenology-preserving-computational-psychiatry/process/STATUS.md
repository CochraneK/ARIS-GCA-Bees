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
- [x] Adversarial audit and expanded novelty audit completed.
- [x] DAIS-C selected as real-clinical open Pilot-0 corpus.
- [x] Official DAIS-C archive automatically downloaded and checksummed.
- [x] Public workflow blocks raw psychiatric transcript publication.
- [x] 28 full-interaction transcripts structurally recovered.
- [x] 1,908 microepisodes inventoried; one-turn rule rejected as too granular.
- [x] 20/40/80-word segmentation sensitivity completed.
- [x] 20- and 40-word strategies advanced to blinded human calibration.
- [x] Private local 140-item A/B calibration packet generator implemented.
- [x] Aggregate Gwet-AC1 scorer implemented.
- [x] Real-DAIS-C boundary-packet smoke workflow passed end-to-end.
- [x] Smoke workflow deletes private text and finishes with a clean Git working tree.
- [x] DAIS-C disease-effect interpretation limits frozen.
- [x] AMP-SCZ Release-4 Pilot-1 minimum-access plan drafted.
- [x] AMP-SCZ variable-family request map drafted with data minimization.

## Current empirical facts from Pilot-0

### Source layer

- 28 usable full-interaction transcripts in the public archive layer;
- raw texts remain outside Git;
- full-interaction participant-word scale matches the speaker-only representation closely enough for engineering use.

### Microepisode layer

- 1,908 interviewer-anchored candidate units;
- 1,871 with participant response;
- participant words median 14, IQR 2–50.

Conclusion: turn-pair units are too often trivial for source-reconstruction fidelity.

### Segmentation sensitivity

- target 20 → 953 windows; median 52 participant words; median 1 microepisode/window;
- target 40 → 745 windows; median 79 words; median 2 microepisodes/window;
- target 80 → 550 windows; median 116 words; median 3 microepisodes/window.

20 and 40 proceed to human boundary calibration. 80 is held as a rescue condition.

## Gate A — novelty

**Conditional pass for research development.**

Formal manuscript-stage multi-database screening remains required.

## Gate B — source engineering

**Passed for DAIS-C Pilot-0.**

Data retrieval, structural classification, segmentation sensitivity, privacy controls and
private calibration-pack generation have all run successfully on real source data.

## Gate C — human boundary calibration

**Current blocker.**

Need two independent raters to complete the blinded 20-vs-40 packet.

Primary outputs:

- coherent boundary;
- sufficient information for a nontrivial query;
- mixed-topic judgment;
- keep/merge/split/reject;
- Gwet AC1.

## Gate D — query / relation calibration

After segmentation is frozen:

- construct source-only queries;
- estimate answerability and redundancy;
- calibrate relation annotation;
- estimate evaluator variance;
- test R3P/R4P projection feasibility.

## Gate E — DAIS-C representation benchmark

Run R0/R1/R2-lite/R3P/R4P as an engineering benchmark.

DAIS-C is not an EASE corpus and is not used for schizophrenia-vs-control disease-effect inference.

## Gate F — AMP-SCZ Pilot-1

**Design/access plan ready.**

Tiered request:

1. transcripts + PSYCHS + minimal linkage/covariates;
2. derived EMA/actigraphy/phone context;
3. derived EEG/imaging;
4. raw high-dimensional modalities only if later hypotheses require them.

The public Release-4 availability record supports open/PSYCHS language structures,
PSYCHS through month 3, smartphone survey/sensors, actigraphy, EEG features and imaging
structures.

Controlled-access data require approved NDA access and must never enter public ARIS4C.

## Gate G — 009A2 randomized acquisition study

Purpose-collected human study remains separate and requires ethics approval.

## Current blocker

The irreducible near-term input is **two independent human raters** for DAIS-C boundary calibration.

All currently automatable Pilot-0 engineering gates are operational.

## Scope control

009A1 = encoding measurement.  
009A2 = acquisition measurement.  
009B = cross-level mechanism.  
009C = longitudinal idiographic dynamics.  
009D = perturbation/intervention validation.
