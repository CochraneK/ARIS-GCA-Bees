# ARIS Status · Language Periodic System

**Candidate:** `language-periodic-system`  
**Branch:** `research/language-periodic-system-aris`  
**ARIS lock:** v0.4.26  
**Paper ID:** not assigned  
**Overall state:** ACTIVE CANDIDATE — Stage 1B robustness / non-periodic reframe under test

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
| research-refine | DRAFTED / evidence-updated | `refine-logs/FINAL_PROPOSAL.md` |
| experiment-plan | ACTIVE | `refine-logs/EXPERIMENT_PLAN.md`, `refine-logs/EXPERIMENT_TRACKER.md` |

## Why the formal ARIS gate is not marked PASS

ARIS v0.4.26 treats novelty-check and research-review as reviewer-bearing phases. A heading or primary-agent critique is not sufficient: the pipeline expects an actual identity-bearing secondary reviewer verdict/trace. No such independent reviewer has been invoked in this ChatGPT-side pass, so we do not fabricate a receipt or claim completion.

## Scientific state

### Stage 0 · prerequisite signal

`MIXED_SIGNAL`.

- 20-component observed compression: 0.510 vs null mean 0.362 (+0.148).
- Pairwise residual association is weak for most pairs but has a substantial upper tail.
- Interpretation: enough non-random structure to justify model comparison; no evidence yet for periodicity.

### Stage 1 · direct model competition

`REFRAME_NONPERIODIC_GEOMETRY`.

On 60 well-covered TLI features:

- random-split Spearman: tree 0.199, graph 0.205, low-rank 0.172, circular 0.122;
- family-held-out Spearman: tree **0.178**, graph 0.163, low-rank/euclidean 0.150, circular **0.109**;
- circular ordering remains moderately reproducible: family-held-out stability **0.542 ± 0.139**.

Interpretation: the simple global circle is not arbitrary, but it currently predicts held-out cross-linguistic structure worse than a hierarchical/tree representation. This is a reason to reframe, not yet a sufficient rejection of the periodic hypothesis.

### Stage 1B · periodic fairness robustness

**RUNNING.**

The robustness test addresses the two clearest attacks on Stage 1:

1. the spectral affinity graph was not fully connected;
2. the circular positions were inherited from a spectral embedding rather than directly optimized for a circular model.

Stage 1B therefore forces a connected affinity, directly optimizes angular feature positions, repeats family-held-out evaluation, and checks two feature counts (40 / 60).

## Novelty after stronger prior-art search

The strongest collision is the Port/Marcolli program:
- *Persistent Topology of Syntax* (2018)
- *Topological Analysis of Syntactic Structures* (2022)

Therefore topology, H1 loops, and geometry of syntax cannot be headline novelty. The surviving wedge is explicit predictive model competition for the periodic-table hypothesis using modern curated global data and genealogy/area-aware evaluation.

## Current likely framing

If Stage 1B confirms the current pattern, shift from “constructing a periodic system” to:

> **Beyond the Periodic Table: Predictive Geometry of Cross-Linguistic Structural Space**

with Baker's periodic-table proposal as the historical hypothesis being tested rather than the result being assumed.

If the optimized periodic model becomes competitive, retain:

> **Testing the Periodic-Table Hypothesis of Human Language**

and continue stronger periodic/non-periodic discrimination.

## Promotion rule

Do not create `papers/002-*` until:

- Stage 1B establishes a fair periodic baseline;
- closest-prior-work search remains clear enough;
- formal ARIS secondary review evidence exists;
- genealogy/geography-aware validation is adequate for the final wording;
- the final framing is frozen as positive periodic, local periodic, non-periodic geometry, or parked.
