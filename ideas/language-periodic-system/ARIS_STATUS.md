# ARIS Status · Language Periodic System

**Candidate:** `language-periodic-system`  
**Canonical branch:** `main`  
**Merged confirmatory source:** `research/language-geometry-confirmatory` via PR #4  
**ARIS lock:** v0.4.26  
**Paper ID:** `002`  
**Overall state:** PROMOTED — formal Paper 002 · manuscript preparation

## Pipeline alignment

ARIS idea-discovery order:

`research-lit → idea-creator → novelty-check → research-review → research-refine-pipeline`

| Phase | State | Durable evidence |
|---|---|---|
| Research brief | DONE | `RESEARCH_BRIEF.md` |
| research-lit | DONE (primary pass + stronger prior-art pass) | `idea-stage/IDEA_REPORT.md` |
| idea-creator | DONE | `idea-stage/IDEA_REPORT.md#ranked-ideas` |
| novelty-check | PASS — independent reviewer accepted novelty wedge | `idea-stage/IDEA_REPORT.md#novelty-verification` |
| research-review | **PASS — WorkBuddy / Tencent Hy3 receipt** | `refine-logs/REVIEW_SUMMARY.md`, `refine-logs/SECONDARY_REVIEW_PACKET.md` |
| research-refine | CONFIRMATORY REFRAME COMPLETE | `refine-logs/FINAL_PROPOSAL.md` |
| experiment-plan | CONFIRMATORY SCREEN COMPLETE | `refine-logs/EXPERIMENT_TRACKER.md` |

## Formal ARIS gate

**PASSED.** WorkBuddy reviewed the candidate in a fresh session using Tencent **Hy3 / Hunyuan**, a different model family from the OpenAI GPT primary executor. The reviewer returned `PASS` and `Promotion authorization: AUTHORIZED`.

Receipt:
- `refine-logs/SECONDARY_REVIEW_RECEIPT.md`
- `refine-logs/SECONDARY_REVIEW_RECEIPT.json`

Formal paper:
- `../../papers/002-language-geometry/`

Reviewer-imposed manuscript requirements remain binding after promotion.

## Scientific state

### Stage 0 · prerequisite structure

`MIXED_SIGNAL`.

TLI contains non-random compressibility and residual feature association, justifying geometry tests but not supporting periodicity by itself.

### Stage 1 / 1B · global predictive competition

The initial and fairness-improved screens show that a simple global circle contains some reproducible structure but does not robustly dominate non-periodic alternatives.

At 60 TLI features, optimized circular remains below tree/low-rank under family hold-out.

### Stage 1C · predefined subsystem screen

`NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE`.

No TLI-defined Grammar / Grammatical categories / Lexical / Phonology domain simultaneously met the predeclared predictive-competitiveness and circular-stability thresholds.

### Stage 1D · direct circularity sensitivity

`CIRCULAR_ROBINSON_NOT_SUPPORTED`.

Held-out circular-Robinson-style row-unimodality deviation is not better than the tree order, and the 60-feature wrap-around closure/internal-adjacency ratio is only **0.037**. This weakens the periodic interpretation directly, rather than only because a richer competitor wins.

### Stage 1E / 1G · geography sensitivity

TLI shows severe loss of association transfer under large geographic blocks. Matched-size random calibration shows this is not explained merely by smaller test samples.

However, this geographic-collapse result is **not universal**: WALS later shows much stronger cross-Macroarea transfer. Geography/area therefore remains a representation-dependent secondary result, not the headline contribution.

### Stage 1F · repeated family-held-out uncertainty

`TREE_ADVANTAGE_STABLE`.

Across 20 TLI family-held-out splits:

- tree 0.182 ± 0.047;
- optimized circular 0.109 ± 0.030;
- tree − circular = **+0.073**;
- 95% bootstrap CI **[0.055, 0.092]**;
- tree win fraction **1.00**.

Low-rank also beats circular on average, so the negative circular result is not based on one tree comparison alone.

### Stage 1H · GBI alternative-curation replication

`TREE_REPLICATES_OVER_CIRCULAR__WEAK_CROSS_MACROAREA_TRANSFER`.

On 1,140 GBI languages / 60 features:

- tree 0.122 ± 0.038;
- circular 0.073 ± 0.036;
- tree win fraction 1.00;
- mean Macroarea association transfer 0.144 ± 0.043.

This is curation robustness, not a fully independent data source.

### Stage 1I · WALS external sanity replication

`WALS_TREE_OVER_CIRCULAR`.

On 2,659 WALS languages / 30 best-covered parameters:

- tree 0.603 ± 0.026;
- circular 0.410 ± 0.050;
- tree − circular = +0.193;
- tree win fraction 1.00 across 8 valid splits.

WALS Macroarea association transfer is high (0.634 ± 0.075), showing that the TLI/GBI geographic-collapse result is not externally stable.

## Current synthesis

The strongest defensible result is:

> **The simple global circular form of the language periodic-table hypothesis is not supported by held-out predictive or direct circularity evidence. Hierarchical/non-circular structure is a stronger family-held-out benchmark across TLI, GBI, and WALS, but the study does not establish one universal tree geometry.**

The project should remain motivated by Baker's historical hypothesis rather than pivoting to a generic “genealogy/geography matters” claim, because strong genealogy/space effects already have major prior art in Grambank and related work.

## Capacity boundary

See `refine-logs/MODEL_CAPACITY_NOTE.md`.

Tree/graph models are not exactly capacity-matched to a single circle, so tree superiority alone cannot prove a universal tree geometry. The negative periodic conclusion is supported additionally by direct optimization, predefined-domain tests, circular-Robinson/closure diagnostics, low-rank comparisons, repeated split uncertainty, and cross-representation replication.

## Post-promotion stage

The idea-stage promotion gate is complete. Remaining work belongs to **Paper 002 manuscript preparation**, not candidate screening.

Mandatory reviewer requirements are mirrored in:
`../../papers/002-language-geometry/process/REVIEW_REQUIREMENTS.md`

## Promotion record

Promoted to **Paper 002 · `papers/002-language-geometry/`** after independent WorkBuddy / Tencent Hy3 `PASS`.
