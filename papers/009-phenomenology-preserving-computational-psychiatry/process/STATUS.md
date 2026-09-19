# ARIS4C009 · Status

**Last updated:** 2026-09-19  
**Current stage:** empirical Pilot-0 / multi-model AI boundary-calibration gate  
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
- [x] 20- and 40-word strategies advanced to blinded calibration.
- [x] Private local 140-item A/B primary/stress packet generator implemented.
- [x] 20 disjoint real-data dry-run windows included.
- [x] Aggregate agreement scorer implemented.
- [x] Pre-AI-redesign real-DAIS-C packet/scorer smoke workflow passed.
- [x] Smoke workflow has read-only repository permission and deletes private text.
- [x] PR #90 updated the smoke workflow to three mock AI judges; post-PR90 workflow success has not yet been independently observed through the GitHub connector.
- [x] Boundary-judge manual and synthetic practice cases completed.
- [x] DAIS-C disease-effect interpretation limits frozen.
- [x] AMP-SCZ Release-4 Pilot-1 minimum-access plan and variable-family map drafted.
- [x] Human-rater requirement retired; Gate C redesigned as multi-model AI judge calibration.

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

20 and 40 proceed to blinded multi-model AI calibration. 80 remains a rescue condition.

## Gate A — novelty

**Conditional pass for research development.**

Formal manuscript-stage multi-database screening remains required.

## Gate B — source engineering

**Passed for DAIS-C Pilot-0.**

All source, privacy, segmentation and private-packet engineering steps have run successfully on real data.

## Gate C — multi-model AI boundary calibration

Human raters are no longer required for Pilot-0.

Primary design:

1. freeze one judge prompt and output schema;
2. use at least three materially different model families/providers where feasible;
3. each judge receives the same blinded items independently, with no access to other judges' outputs;
4. deterministic/low-variance decoding is preferred;
5. record model/provider/version/date and data-handling mode;
6. compute multi-judge Gwet AC1 plus all pairwise AC1 values;
7. compare strategy usability by blinded condition;
8. use majority and unanimous consensus only as engineering summaries, not human reliability evidence.

Primary outputs:

- coherent boundary;
- sufficient nontrivial information;
- mixed-topic judgment;
- keep/merge/split/reject;
- confidence;
- multi-model agreement and pairwise disagreement structure.

The paper must call this **AI-judge agreement** or **cross-model agreement**, never human inter-rater reliability.

## Gate D — query / relation calibration

After segmentation is frozen:

- construct source-only queries;
- estimate answerability and redundancy;
- calibrate relation annotation;
- estimate evaluator variance;
- test R3P/R4P projection feasibility.

## Gate E — DAIS-C representation benchmark

Run R0/R1/R2-lite/R3P/R4P as an engineering benchmark.

No schizophrenia-vs-control disease-effect inference is permitted from this Pilot-0 because acquisition/topic structure differs between groups.

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

Deletion-safe recovery file: `process/CHAT_HANDOFF_2026-09-19.md`.

There is no longer a human-rater blocker.

The remaining Gate-C implementation task is:

> **run the frozen private packet through at least three approved, materially different AI judge models and score the resulting cross-model agreement.**

If external APIs are used, DAIS-C source text must only be sent through endpoints whose data-use/retention terms are compatible with the dataset and project governance. Local models are acceptable.

## Scope control

009A1 = encoding measurement.  
009A2 = acquisition measurement.  
009B = cross-level mechanism.  
009C = longitudinal idiographic dynamics.  
009D = perturbation/intervention validation.


## Handoff sentence

If this chat is lost, resume from `process/CHAT_HANDOFF_2026-09-19.md` plus this file. **Do not redesign 009.** The next empirical step is the actual three-or-more-model blinded Gate-C run; only after those judge outputs are frozen should the project select 20 vs 40 words and advance to Gate D.
