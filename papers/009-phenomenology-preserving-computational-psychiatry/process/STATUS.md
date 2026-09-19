# ARIS4C009 · Status

**Last updated:** 2026-09-19  
**Current stage:** empirical Pilot-0 / Gate D query-relation calibration next  
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
- [x] PR #90 updated the smoke workflow to three mock AI judges; the post-PR90 run on `main` succeeded (2026-09-19T05:38:03Z).
- [x] Boundary-judge manual and synthetic practice cases completed.
- [x] DAIS-C disease-effect interpretation limits frozen.
- [x] AMP-SCZ Release-4 Pilot-1 minimum-access plan and variable-family map drafted.
- [x] Human-rater requirement retired; Gate C redesigned as multi-model AI judge calibration.
- [x] AI judge executor implemented (`run_ai_boundary_judges.py`): frozen prompt, resumable, fail-closed.
- [x] Private dry run on the 20 disjoint training windows completed before any primary item was scored.
- [x] Frozen 140-item packet rated end-to-end by three materially different model families (140/140 each, 0 failures).
- [x] Cross-model agreement scored, including leave-one-judge-out and stress-stratum checks.
- [x] Aggregate-only publication step added (`publish_boundary_ai_calibration.py`) plus AI-judge audit workflow.
- [x] Gate C executed and segmentation strategy selected; results documented.

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

20 and 40 proceed to blinded multi-model AI calibration; the Gate-C run below selected 40.
80 remains a rescue condition.

### Boundary calibration (Gate C, executed 2026-09-19)

Three complete, blinded AI judges on 120 regular windows: `gpt-oss-120b`, `nemotron-3-ultra`,
`stepfun-3.7-flash`. Multi-model Gwet AC1: sufficient-nontrivial 0.9525, mixed-topics 0.9340,
coherent-boundary 0.7425, recommended-action 0.7416.

Selected strategy: **40-word target**. Windows built to that target needed repair (merge/split/
reject) from a judge majority on 8.33% of items versus 18.33% at the 20-word target, and drew zero
majority insufficiency flags versus 3.33%. No "revise segmentation" clause in the protocol fired.
The realised-size difference is small (median 88 vs 76 participant words), so the usual
lower-bandwidth argument for 20 words largely disappears in practice.

`coherent_boundary` agreement is the weakest measurement in the gate and is carried forward as a
named limitation: downstream boundary labels must be ≥2-of-3 model consensus, never a single-judge
or expert verdict. Full record: `AI_JUDGE_CALIBRATION_RESULTS_2026-09-19.md`.

## Gate A — novelty

**Conditional pass for research development.**

Formal manuscript-stage multi-database screening remains required.

## Gate B — source engineering

**Passed for DAIS-C Pilot-0.**

All source, privacy, segmentation and private-packet engineering steps have run successfully on real data.

## Gate C — multi-model AI boundary calibration

**Executed on 2026-09-19: passed as an engineering calibration gate.**

Human raters are not required for Pilot-0, and this gate does not substitute for them: what was
measured is cross-model agreement under a frozen rubric.

Design as executed:

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

**Next.** Segmentation is now frozen at the 40-word target, so this gate can start.

Before that work begins:

- construct source-only queries;
- estimate answerability and redundancy;
- calibrate relation annotation;
- estimate evaluator variance;
- test R3P/R4P projection feasibility.

Gate D must also decide the two open items Gate C handed forward: whether boundary labels are
derived by ≥2-of-3 model consensus (recommended, given AC1 0.74 on `coherent_boundary`), and
whether the extra realised words in 40-word windows actually buy answerable queries.

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

Gate C no longer blocks the pipeline, and the human-rater blocker it replaced stays retired: the
frozen packet has been rated and scored.

What actually blocks progress now:

1. **Gate D has no implementation yet.** Query construction, answerability/redundancy estimation
   and relation annotation are specified on paper but have no code or run record.
2. **Endpoint governance is unresolved.** The Gate-C judges ran through a local loopback gateway
   whose routes include hosted upstream inference; no route was verified zero-retention. If the
   stricter local-only reading of the privacy rule is adopted, Gate C must be re-run against a
   fully local endpoint and the results document superseded, not edited.
3. **Judge capacity.** Three of six started model families could not finish because the shared
   gateway returned sustained HTTP 429 and two routes vanished mid-run. A future gate that needs
   ≥5 independent judges requires either quota headroom or a local serving path.
4. **Human interpretability remains untested.** Gate C replaced the human-rater blocker with a
   cross-model robustness check; it did not produce evidence that a clinician or the interviewee
   would find these windows coherent. Any claim needing that must be a separate study.
5. Gate G still requires ethics approval; Gate F still waits on AMP-SCZ access.

## Scope control

009A1 = encoding measurement.  
009A2 = acquisition measurement.  
009B = cross-level mechanism.  
009C = longitudinal idiographic dynamics.  
009D = perturbation/intervention validation.


## Handoff sentence

If this chat is lost, resume from `process/CHAT_HANDOFF_2026-09-19.md` plus this file. **Do not redesign 009.** Gate C has now run: the frozen packet was rated by three blinded model families and the 40-word segmentation target was selected, so the project must not reopen the 20-vs-40 choice. The next empirical step is implementing Gate D — source-only query construction, answerability/redundancy estimation and relation annotation — using ≥2-of-3 model consensus for any boundary label.
