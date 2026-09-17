# Experiment Tracker · Language Periodic System

| ID | Experiment | Status | Decision role | Artifact |
|---|---|---|---|---|
| S0-A | Compression vs marginal-preserving shuffle | DONE | prerequisite structural signal | `../PILOT_REPORT.md` |
| S0-B | Residual pairwise NMI vs permutation null | DONE | prerequisite residual dependency | `../PILOT_REPORT.md` |
| S1-A | Random-split geometric model competition | DONE | optimistic held-out screen | `../STAGE1_REPORT.md` |
| S1-B | Glottolog family-held-out model competition | DONE | genealogy-aware screen | `../STAGE1_REPORT.md` |
| R1 | Connected-affinity sensitivity | DONE | remove spectral disconnect artifact | `../STAGE1B_REPORT.md` |
| R2 | Directly optimized circular model | DONE | rule out obvious circular strawman | `../STAGE1B_REPORT.md` |
| R3 | 40/60 feature-count sensitivity | DONE | robustness to feature count | `../STAGE1B_REPORT.md` |
| R4 | Predefined TLI-domain local periodicity screen | DONE | test local periodicity without cherry-picking | `../STAGE1C_REPORT.md` |
| R5 | Circular-Robinson + wrap-around closure sensitivity | DONE | direct periodic/circular diagnostic | `../STAGE1D_REPORT.md` |
| R6 | Repeated family-held-out paired uncertainty | DONE | quantify tree/low-rank vs circle stability | `../STAGE1F_REPORT.md` |
| R6b | Model-capacity accounting | DONE / interpretive | prevent tree-win overclaim | `MODEL_CAPACITY_NOTE.md` |
| R7 | Geographic and joint geography+family blocking | DONE | area-aware stress test | `../STAGE1E_REPORT.md` |
| R7b | Matched-size geographic calibration | DONE | separate geographic shift from small-test noise | `../STAGE1G_REPORT.md` |
| R8a | GBI alternative-curation replication | DONE | robustness to dependency curation | `../STAGE1H_REPORT.md` |
| R8b | WALS external sparse sanity replication | DONE | external qualitative direction check | `../STAGE1I_REPORT.md` |
| ARIS-REV | Identity-bearing secondary novelty/research review | **PENDING / ONLY HARD GATE** | formal ARIS review gate | `SECONDARY_REVIEW_PACKET.md` |

## Evidence trajectory

### Stage 0
`MIXED_SIGNAL`: non-random compressibility and residual associations justify a geometry question.

### Stage 1 / 1B
A simple global circle is reproducible but generally underpredicts tree/low-rank alternatives under family hold-out. Direct angular optimization prevents the first circle from being dismissed as an obvious strawman.

### Stage 1C
`NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE`: no predefined TLI subsystem satisfies both predictive competitiveness and circular-order stability.

### Stage 1D
`CIRCULAR_ROBINSON_NOT_SUPPORTED`: the learned circular order does not achieve strong held-out row-unimodality improvement and lacks robust wrap-around closure, especially at 60 features (closure/internal-adjacency ratio ≈0.037).

### Stage 1F
`TREE_ADVANTAGE_STABLE`: across 20 TLI family-held-out splits, tree beats optimized circular in every split. Mean paired difference +0.073; 95% bootstrap CI [0.055, 0.092]. Low-rank also beats circular on average.

### Stage 1E / 1G
TLI association structure transfers poorly across large geographic blocks, and matched-size random calibration shows this is not simply small-test noise. This cannot become the headline result because external WALS behaves differently.

### Stage 1H
GBI replicates the family-held-out tree-over-circle ordering (tree 0.122 vs circular 0.073; win fraction 1.00) and weak Macroarea transfer (0.144).

### Stage 1I
WALS independently reproduces the tree-over-circle ordering (0.603 vs 0.410; win fraction 1.00), but **does not** reproduce weak Macroarea transfer (mean 0.634). This sharply separates the robust negative-periodicity result from the representation-dependent geography result.

## Current branch decision

**Confirmatory screening is complete.**

The strongest claim is not “language is tree-shaped.” It is:

> **The tested simple global circular/periodic geometry is not supported; hierarchical/non-circular models provide stronger family-held-out predictive benchmarks across TLI, GBI, and WALS.**

A generic genealogy/geography paper is not the right reframe because genealogy/space effects already have strong prior art, and WALS shows that geographic portability is dataset-sensitive.

## Promotion gate

The candidate is scientifically mature enough for formal review but remains unnumbered until:

- ARIS-REV produces a real identity-bearing secondary reviewer trace;
- the reviewer finds no fatal prior-art collision with the full predictive periodic-vs-nonperiodic stress test;
- the reviewer accepts the model-fairness and claim-boundary logic, or requests tractable revisions.

If those conditions are met, promote to the next stable Paper ID and begin manuscript-generation / review loops. Do not consume Paper 002 before that gate.
