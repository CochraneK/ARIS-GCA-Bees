# Final Proposal · Beyond the Periodic Table

**Working title:** *Beyond the Periodic Table: Predictive Geometry of Cross-Linguistic Structural Space*  
**Historical hypothesis:** *Testing the Periodic-Table Hypothesis of Human Language*  
**Status:** `REVISE` — reframe supported by exploratory evidence; confirmatory controls and formal ARIS secondary review pending  
**Candidate:** `language-periodic-system`  
**Paper ID:** not assigned

## Problem Anchor

Mark C. Baker's 2001 “periodic table of languages” proposed that a finite set of grammatical parameters might organize language diversity in a systematic way analogous to chemistry. Modern global typological data make a stronger and falsifiable question possible:

> **What geometry best predicts cross-linguistic structural relations, and does a genuinely periodic representation add reproducible value beyond non-periodic alternatives?**

The project does not build a periodic table by visual analogy. It treats periodicity as a model class that can lose.

## Refined Thesis

Current evidence supports **structured but predominantly non-periodic predictive geometry** rather than a single global language periodic table. Circular representations repeatedly capture some reproducible structure, but they have not been the best predictive representation globally or within any predefined TLI subsystem under family-held-out screening.

The paper should therefore keep Baker's periodic-table proposal as the historically motivated hypothesis and make the empirical contribution a predictive comparison of geometric descriptions of linguistic design space.

## Dominant Contribution

**An explicit out-of-sample model competition for the historical language-periodic-table hypothesis on modern dependency-curated cross-linguistic data, with evidence used to identify a better-performing structural geometry rather than forcing the periodic analogy.**

This is narrower than claiming to discover linguistic atoms, global topology, or typological feature prediction, all of which have substantial prior art.

## Prior-Art Boundary

- Baker (2001): periodic-table metaphor and parameter hierarchy already exist.
- Port et al. (2018) and Port, Karidi & Marcolli (2022): topology and persistent H1 loops in syntactic-parameter spaces already exist.
- Grambank (2023): PCA, feature bundles, and latent classes over global morphosyntax already exist.
- Graff et al. (2025): dependency-curated GBI/TLI data provide the modern substrate used here.
- Verkerk et al. (2025/2026): grammatical universals already receive phylogenetic/spatial testing.
- SIGTYP/computational typology: held-out typological prediction is already established.
- Armstrong, Guzmán & Sing-Long (2021) and related circular-seriation work: circular Robinson matrices provide a formal standard for circular-order claims and motivate one remaining fairness check.

The novelty claim must therefore remain **predictive hypothesis competition**, not any one ingredient above.

## Evidence Ladder

### Stage 0 · non-random structure exists

`MIXED_SIGNAL` on 644 TLI languages.

- 20-component observed compression: 0.510 vs shuffle-null 0.362 (+0.148).
- Pairwise residual association is weak for most feature pairs but has a substantial upper tail.

This justified geometry testing but did not support periodicity.

### Stage 1 · simple global periodicity loses

`REFRAME_NONPERIODIC_GEOMETRY`.

Family-held-out mean Spearman on 60 features:

- tree 0.178;
- graph 0.163;
- low-rank / Euclidean 0.150;
- circular 0.109.

Circular ordering was moderately reproducible (0.542 ± 0.139), so the result is not “no structure”; it is “the simple circle leaves predictive information unexplained.”

### Stage 1B · fairer circle gives a mixed robustness result

`MIXED_ROBUSTNESS`.

After forcing connected affinity and directly optimizing angular positions:

- 40 features: optimized circular 0.179, tree 0.178, Euclidean 0.217, stability 0.419;
- 60 features: optimized circular 0.105, tree 0.147, low-rank 0.153, stability 0.628.

This rules out the strongest “your circular model was obviously too weak” objection, while also showing that apparent periodic competitiveness is sensitive to feature selection/coverage.

### Stage 1C · predefined domains do not rescue local periodicity

`NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE`.

TLI's own grouping metadata predefine five domains. Each report contains four valid top-level-family-held-out replicates.

- Grammar linear order: circle 0.401, tree 0.494, circular stability 0.811.
- Grammar other: circle 0.253, tree 0.313, stability 0.274.
- Grammatical categories: circle 0.252, tree 0.229, stability 0.373 — ambiguous, below the predeclared stability threshold.
- Lexical: circle 0.142, tree 0.269, stability 0.057.
- Phonology: circle 0.151, tree 0.229, stability 0.550.

No predefined subsystem met both predictive-competitiveness and stability criteria for local periodicity.

## Main Hypotheses Going Forward

### H0 · Most apparent geometry is inheritance/contact leakage
Structured models lose much of their predictive value under stronger phylogenetic/geographic blocking.

### H1 · A standards-aligned periodic geometry remains competitive
A circular-seriation / circular-Robinson-compatible model yields out-of-sample value comparable to the best non-periodic model after fair capacity control.

### H2 · Structured but non-periodic geometry dominates
Tree/low-rank/graph or another non-periodic representation retains a reproducible advantage under family, geography, and replication tests.

### H3 · Narrow mixed structure
Specific subsystems exhibit stable circular orderings without a full periodic predictive geometry. Grammar linear order is a possible example of stable order without best-in-class circular prediction.

Current exploratory evidence favors **H2**, with H3 plausible as a descriptive nuance.

## Remaining Decisive Tests

1. **Standards-aligned circular seriation:** use a circular-Robinson / circular-seriation criterion or implementation rather than relying only on custom spectral/optimized circle models.
2. **Uncertainty / capacity:** increase repeated family-held-out evaluation and report paired model-difference intervals; document effective model complexity.
3. **Geography:** add areal/geographic blocking or comparable spatial sensitivity.
4. **Replication:** reproduce the main ranking on a second dataset or independent feature subset.
5. **Formal ARIS secondary review:** obtain a real identity-bearing reviewer trace; do not self-certify.

## Complexity Intentionally Rejected

- No decorative periodic table as a result.
- No claim that typological features are chemical-like atoms or universal natural kinds.
- No persistent-homology novelty claim.
- No torus or multi-cycle model unless standards-aligned circular testing gives a reason to pursue richer periodicity.
- No missing-cell/Mendeleev prediction until a validated generative structure exists.
- No expensive frontier model is required for the core empirical analysis.

## Decision Logic

### If the standards-aligned periodic baseline becomes competitive
Retain the historical-hypothesis title and report a genuinely mixed geometry result.

### If non-periodic models retain the advantage
Use *Beyond the Periodic Table: Predictive Geometry of Cross-Linguistic Structural Space* and present the periodic-table proposal as an empirically constrained historical hypothesis.

### If all models collapse under geography/phylogeny-aware validation
Park the candidate or publish only if the methodological leakage result itself becomes strong and novel enough.

## Manuscript Claim Boundary

Even a successful study must not claim that:

- linguistic features are chemical elements;
- statistical geometry proves universal grammar;
- association geometry is causal;
- family-held-out splits fully solve phylogenetic/contact dependence;
- unattested combinations are impossible languages;
- the periodic hypothesis is decisively rejected before standards-aligned seriation and spatial/replication checks.

## Promotion Decision

**Do not assign Paper 002 yet.** The candidate has matured enough to justify continued ARIS work, but manuscript identity should remain unfrozen until the remaining confirmatory controls and formal reviewer gate are complete.
