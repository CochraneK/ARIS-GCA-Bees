# ARIS Status · Language Periodic System

**Candidate:** `language-periodic-system`  
**Branch:** `research/language-periodic-system-aris`  
**ARIS lock:** v0.4.26  
**Paper ID:** not assigned  
**Overall state:** ACTIVE CANDIDATE — Stage 1 experiment implementation

## Pipeline alignment

ARIS idea-discovery order:

`research-lit → idea-creator → novelty-check → research-review → research-refine-pipeline`

| Phase | State | Durable evidence |
|---|---|---|
| Research brief | DONE | `RESEARCH_BRIEF.md` |
| research-lit | DONE (primary pass) | `idea-stage/IDEA_REPORT.md#literature-landscape` |
| idea-creator | DONE (scope variants ranked) | `idea-stage/IDEA_REPORT.md#ranked-ideas` |
| novelty-check | DONE as primary-executor search; FORMAL REVIEW RECEIPT PENDING | `idea-stage/IDEA_REPORT.md#novelty-verification` |
| research-review | PENDING formal secondary ARIS reviewer | `idea-stage/IDEA_REPORT.md#external-critical-review` contains only primary stress test |
| research-refine-pipeline | DRAFTED, NOT GATED | `refine-logs/EXPERIMENT_PLAN.md` |

## Why the formal ARIS gate is not marked PASS

ARIS v0.4.26 treats novelty-check and research-review as reviewer-bearing phases. A heading or primary-agent critique is not sufficient: the pipeline expects an actual identity-bearing secondary reviewer verdict/trace. No such independent reviewer has been invoked in this ChatGPT-side pass, so we do not fabricate a receipt or claim completion.

## Scientific state

### Stage 0
`MIXED_SIGNAL`.

- 20-component observed compression: 0.510 vs null mean 0.362 (+0.148).
- Pairwise residual association is weak for most pairs but has a substantial upper tail.
- Interpretation: enough non-random structure to justify model comparison; zero evidence yet for periodicity.

### Novelty after stronger prior-art search

The strongest collision is the Port/Marcolli program:
- Persistent Topology of Syntax (2018)
- Topological Analysis of Syntactic Structures (2022)

Therefore topology, H1 loops, and geometry of syntax cannot be headline novelty. The surviving wedge is explicit predictive model competition for the periodic-table hypothesis using modern curated global data and genealogy/area-aware evaluation.

## Next executable milestone

Implement Stage 1A:

1. derive train/test feature-association matrices from TLI;
2. compare null, Euclidean low-rank, hierarchical/tree, graph-distance, and circular periodic models;
3. score prediction of held-out associations;
4. add Glottolog family-held-out splits;
5. use bootstrap stability to decide GO / REFRAME / STOP.

## Promotion rule

Do not create `papers/002-*` until:

- Stage 1 produces a scientifically interpretable result;
- closest-prior-work search remains clear enough;
- formal ARIS secondary review evidence exists;
- the final framing is frozen as either a periodic-system result or a broader design-space-geometry result.
