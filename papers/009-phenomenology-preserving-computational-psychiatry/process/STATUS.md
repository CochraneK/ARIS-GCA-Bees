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
- [x] Private local 140-item A/B primary/stress packet generator implemented.
- [x] 20 disjoint real-data training windows added to the private generator.
- [x] Training windows are excluded from primary agreement estimates.
- [x] Aggregate Gwet-AC1 scorer implemented.
- [x] Real-DAIS-C packet/scorer smoke workflow passed.
- [x] Smoke workflow has read-only repository permission and deletes private text.
- [x] Boundary-rater manual completed.
- [x] Synthetic practice cases and answer key completed.
- [x] DAIS-C disease-effect interpretation limits frozen.
- [x] AMP-SCZ Release-4 Pilot-1 minimum-access plan and variable-family map drafted.

## Current empirical facts from Pilot-0

### Source layer

- 28 usable full-interaction transcripts in the public archive layer;
- raw texts remain outside Git;
- participant-word scale is consistent across full-interaction and speaker-only representations for engineering purposes.

### Microepisode layer

- 1,908 interviewer-anchored candidate units;
- 1,871 with participant response;
- participant words median 14, IQR 2–50.

Turn-pair units are too often trivial for fidelity scoring.

### Segmentation sensitivity

- target 20 → 953 windows; median 52 participant words; median 1 microepisode/window;
- target 40 → 745 windows; median 79 words; median 2 microepisodes/window;
- target 80 → 550 windows; median 116 words; median 3 microepisodes/window.

20 and 40 proceed to human boundary calibration. 80 is a rescue condition only.

## Gate A — novelty

**Conditional pass for research development.**

Formal manuscript-stage multi-database screening remains required.

## Gate B — source engineering

**Passed for DAIS-C Pilot-0.**

All currently automatable source, privacy, segmentation and private-packet engineering
steps have run successfully on real data.

## Gate C — rater training and boundary calibration

**Current blocker.**

Required sequence:

1. two raters read `RATER_MANUAL_BOUNDARY.md`;
2. independently complete synthetic practice;
3. discuss using `RATER_PRACTICE_KEY.md`;
4. independently rate 20 private real-data training windows;
5. discuss/freeze rule;
6. independently rate 140 primary/stress items;
7. run aggregate scorer.

Primary outputs:

- coherent boundary;
- sufficient nontrivial information;
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

No schizophrenia-vs-control disease-effect inference is permitted from this Pilot-0
because acquisition/topic structure differs between groups.

## Gate F — AMP-SCZ Pilot-1

**Design/access plan ready.**

Minimum first request:

- open/PSYCHS language evidence;
- PSYCHS structured measures;
- minimal participant/visit linkage and covariates.

Context and neural modalities are requested only in later tiers.

## Gate G — 009A2 randomized acquisition study

Purpose-collected human study remains separate and requires ethics approval.

## Current blocker

The irreducible near-term input is now exactly:

> **two independent human raters completing the frozen boundary-calibration workflow.**

There is no remaining high-value automated Pilot-0 step before this gate.

## Scope control

009A1 = encoding measurement.  
009A2 = acquisition measurement.  
009B = cross-level mechanism.  
009C = longitudinal idiographic dynamics.  
009D = perturbation/intervention validation.
