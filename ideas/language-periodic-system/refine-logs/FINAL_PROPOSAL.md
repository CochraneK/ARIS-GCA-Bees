# Final Proposal · Testing the Periodic-Table Hypothesis of Human Language

**Status:** `REVISE` pending robustness tests and formal ARIS secondary review  
**Candidate:** `language-periodic-system`  
**Paper ID:** not assigned

## Problem Anchor

Mark C. Baker's 2001 “periodic table of languages” made a memorable theoretical proposal: recurrent grammatical parameters might organize the diversity of human languages in a systematic way analogous to chemical elements. Two decades of typological data collection now make a stronger, falsifiable question possible:

> **Does cross-linguistic structural variation exhibit a genuinely recurrent periodic geometry, or is its design space better described by non-periodic structures?**

The project will not build a periodic table by visual analogy. It will compare explicit geometric hypotheses on held-out data and accept the geometry supported by predictive evidence.

## Final Method Thesis

Treat the periodic-table analogy as a **model class**, not a conclusion. Fit low-capacity periodic representations of cross-linguistic feature relations and compare their out-of-sample performance against null, low-rank/Euclidean, hierarchical, and graph/manifold alternatives under increasingly strict language, family, and geographic hold-outs.

The central output is a discriminating empirical answer to the historical periodic-table hypothesis. A negative result is scientifically meaningful only if the periodic model receives a fair test and the competing geometry generalizes beyond genealogical leakage.

## Dominant Contribution

**The first explicit predictive model competition, located so far, that operationalizes the language-periodic-table hypothesis and tests it against non-periodic alternatives on modern dependency-curated cross-linguistic structural data.**

This contribution is narrower than “discovering linguistic atoms,” “finding topology,” or “predicting typological features,” all of which have substantial prior art.

## Supporting Contributions

1. A reproducible benchmark for geometric models of cross-linguistic feature association using TLI/GBI and Glottolog metadata.
2. A distinction between **structural recurrence** and **periodicity**: non-random organization, clustering, or an H1 loop is not sufficient evidence for a periodic system.
3. If supported, a map of local recurrent modules; if unsupported, an empirically grounded replacement for the periodic-table metaphor.

## Complexity Intentionally Rejected

- No decorative “periodic table” is constructed before the hypothesis survives testing.
- No claim that typological features are universal linguistic atoms or natural kinds.
- Persistent homology is not the headline method because Port/Marcolli already established topology-of-syntax analyses.
- No torus, multi-cycle, deep neural embedding, or generative missing-cell model is added unless the simple circular model leaves reproducible periodic residual structure.
- No frontier LLM is required for the core scientific method.

## Current Evidence

### Stage 0 · prerequisites

TLI-statistical densified-small (644 languages) shows organization beyond an independence-style null:

- 20-component compression: observed 0.510 vs shuffled-null 0.362 (+0.148).
- Residual pairwise NMI is weak for most pairs but has a substantial upper tail.

Verdict: `MIXED_SIGNAL`. This justified direct model comparison but did not support periodicity.

### Stage 1 · first direct screen

The first held-out comparison currently yields `REFRAME_NONPERIODIC_GEOMETRY`:

- circular model mean Spearman ≈ **0.122** under random language splits;
- circular model mean Spearman ≈ **0.109** under top-level-family-held-out splits;
- best non-periodic family-held-out model ≈ **0.178**;
- circular-order stability across family-held-out resampling ≈ **0.542**.

Interpretation: a simple circular ordering is not arbitrary—it shows moderate reproducibility—but it currently leaves predictive structure on the table relative to a non-periodic alternative. This is evidence **against promoting a simple global periodic table at this stage**, not evidence that language lacks structure.

These numbers are screening results. They must be reproduced from the durable `STAGE1_REPORT.md`/JSON output and subjected to robustness checks before entering a manuscript claim.

## Main Hypotheses

### H0 · No robust design-space geometry beyond genealogy/area
All structured models lose most predictive value under family/geographic hold-out.

### H1 · Global periodic geometry
A circular/periodic model provides stable, capacity-controlled predictive value matching or exceeding non-periodic alternatives under family/area hold-out.

### H2 · Structured but non-periodic global geometry
Feature relations generalize across languages and families, but tree/graph/manifold/Euclidean models reliably outperform periodic models.

### H3 · Local periodicity
The global space is non-periodic, but train-discovered structural modules contain reproducible local cyclic organization that generalizes to held-out families.

The current screen favors **H2 over H1**, while H3 remains untested.

## Critical Robustness Requirements

Before treating H1 as rejected rather than merely underfit, run:

1. **Periodic-model fairness:** ensure the circular model is not a strawman; test at least one directly optimized circular latent model in addition to spectral-angle initialization.
2. **Feature-count sensitivity:** repeat with multiple coverage/cardinality thresholds and feature counts.
3. **Split sensitivity:** increase repeated family-held-out runs; report uncertainty on model differences rather than only means.
4. **Affinity/connectivity sensitivity:** remove the disconnected spectral-graph warning or show results are robust to a connected affinity construction.
5. **Geographic control:** add geography-aware blocked validation or equivalent sensitivity analysis.
6. **Dataset/domain replication:** replicate the main conclusion on a second dataset or structural subset where possible.
7. **Capacity accounting:** document free parameters/hyperparameter selection and prevent a more flexible competitor from winning by construction.

## Decision Logic

### If periodic catches up after fairness checks
Retain the title *Testing the Periodic-Table Hypothesis of Human Language* and pursue a positive or mixed periodic-system result.

### If non-periodic models remain clearly superior
Keep the historical hypothesis as the motivating question but make the paper's substantive result the geometry that replaces it. A possible framing is:

> *Beyond the Periodic Table: Predictive Geometry of Cross-Linguistic Structural Space*

### If all models collapse under genealogy/geography controls
Do not force a paper. Park the candidate or reframe as a methodological caution about leakage in global typological geometry.

## Manuscript Claim Boundary

Even a strong result must not claim:

- that linguistic features are chemical-like elements;
- that statistical geometry proves universal grammar;
- that an association geometry is causal;
- that family-held-out validation fully solves phylogenetic or contact dependence;
- that unattested feature combinations are impossible languages.

## Next Action

Run robustness Stage 1B before promotion. Then perform the formal ARIS secondary review. Only after those gates should this candidate receive the next stable ARIS4C Paper ID.
