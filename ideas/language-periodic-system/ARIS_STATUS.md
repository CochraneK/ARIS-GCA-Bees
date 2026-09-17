# ARIS Status · Language Periodic System

**Candidate:** `language-periodic-system`  
**Branch:** `research/language-periodic-system-aris`  
**ARIS lock:** v0.4.26  
**Paper ID:** not assigned  
**Overall state:** ACTIVE CANDIDATE — REFRAME toward predictive geometry; confirmatory controls pending

## Pipeline alignment

ARIS idea-discovery order:

`research-lit → idea-creator → novelty-check → research-review → research-refine-pipeline`

| Phase | State | Durable evidence |
|---|---|---|
| Research brief | DONE | `RESEARCH_BRIEF.md` |
| research-lit | DONE (primary pass) | `idea-stage/IDEA_REPORT.md#literature-landscape` |
| idea-creator | DONE (scope variants ranked) | `idea-stage/IDEA_REPORT.md#ranked-ideas` |
| novelty-check | DONE as primary-executor search; FORMAL REVIEW RECEIPT PENDING | `idea-stage/IDEA_REPORT.md#novelty-verification` |
| research-review | PENDING formal secondary ARIS reviewer | `refine-logs/REVIEW_SUMMARY.md` |
| research-refine | REFRAMED / evidence-updated | `refine-logs/FINAL_PROPOSAL.md` |
| experiment-plan | ACTIVE | `refine-logs/EXPERIMENT_PLAN.md`, `refine-logs/EXPERIMENT_TRACKER.md` |

## Formal ARIS gate

ARIS v0.4.26 treats novelty-check and research-review as reviewer-bearing phases. This run has no identity-bearing secondary-review trace, so the formal review gate remains **PENDING**. No reviewer identity, verdict, or trace is fabricated.

## Scientific state

### Stage 0 · prerequisite signal

`MIXED_SIGNAL`.

- 20-component observed compression: 0.510 vs null mean 0.362 (+0.148).
- Residual pairwise association is weak for most pairs but has a substantial upper tail.
- Conclusion: language structure is non-random enough to justify geometry tests; this is not evidence of periodicity.

### Stage 1 · global model competition

`REFRAME_NONPERIODIC_GEOMETRY`.

On 60 well-covered TLI features:

- random-split Spearman: tree 0.199, graph 0.205, low-rank 0.172, circular 0.122;
- family-held-out Spearman: tree **0.178**, graph 0.163, low-rank/euclidean 0.150, circular **0.109**;
- family-held-out circular-order stability: **0.542 ± 0.139**.

The simple global circle contains reproducible information but predicts less well than non-periodic alternatives.

### Stage 1B · fairer periodic baseline

`MIXED_ROBUSTNESS`.

The disconnected-affinity issue was removed and angular feature positions were optimized directly.

- **40 features:** optimized circular 0.179; tree 0.178; connected Euclidean 0.217; circular stability 0.419.
- **60 features:** optimized circular 0.105; tree 0.147; low-rank 0.153; circular stability 0.628.

Conclusion: the initial circle was not merely a strawman, but periodic competitiveness is feature-count sensitive and does not support a simple global periodic system.

### Stage 1C · predefined subsystem test

`NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE`.

TLI's own grouping metadata were used to predefine Grammar linear order, Grammar other, Grammatical categories, Lexical, and Phonology. Every reported domain contains four valid top-level-family-held-out splits.

- **Grammar linear order:** circular optimized 0.401 with very stable ordering (0.811), but tree/low-rank ≈0.494/0.493 — stable structure, not best represented as a circle.
- **Grammar other:** circular optimized 0.253 vs tree 0.313; stability 0.274.
- **Grammatical categories:** circular optimized 0.252 vs tree 0.229, but stability only 0.373 — ambiguous, below the predeclared periodic-candidate threshold.
- **Lexical:** circular optimized 0.142 vs tree 0.269; stability 0.057.
- **Phonology:** circular optimized 0.151 vs tree 0.229; stability 0.550.

No predefined domain simultaneously met the predictive and stability criteria for local periodicity.

## Current interpretation

The evidence now favors the broader framing:

> **Beyond the Periodic Table: Predictive Geometry of Cross-Linguistic Structural Space**

Baker's periodic-table idea remains the motivating historical hypothesis, but the empirical target is now to identify which non-periodic geometry best generalizes and whether the periodic hypothesis can be rejected fairly after standardized circular-seriation, geography, capacity, and replication checks.

This is **not yet a manuscript-level rejection** of periodicity. Circular seriation has a formal literature built around circular Robinson matrices; one standards-aligned seriation/goodness-of-fit check should be added before closing that hypothesis.

## Remaining decisive gates

1. standards-aligned circular-seriation / circular-Robinson sensitivity;
2. geography-aware blocked validation;
3. stronger repeated-split uncertainty and model-capacity accounting;
4. second-dataset or second-domain replication;
5. identity-bearing ARIS secondary review.

## Promotion rule

Do not create `papers/002-*` yet. Promotion requires the remaining controls to support a stable framing and the formal ARIS review gate to be satisfied honestly.
