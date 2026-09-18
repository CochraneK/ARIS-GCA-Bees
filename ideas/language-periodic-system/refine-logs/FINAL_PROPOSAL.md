# Final Proposal · Testing the Periodic-Table Hypothesis of Human Language

**Current working title:** *Testing the Periodic-Table Hypothesis of Human Language: Predictive Evidence Favors Non-Circular Structure*  
**Alternate title:** *Beyond the Periodic Table: Stress-Testing the Geometry of Cross-Linguistic Structural Space*  
**Status:** `REVIEW_READY_CANDIDATE` — confirmatory screening complete; formal ARIS secondary review still pending  
**Candidate:** `language-periodic-system`  
**Paper ID:** not assigned

## Problem Anchor

Mark C. Baker's 2001 “periodic table of languages” proposed that grammatical parameters could organize language diversity in a systematic way analogous to chemistry. The broad metaphor is not new. Modern global typological resources now permit a sharper question:

> **When periodicity is operationalized as an explicit circular model, does it predict cross-linguistic structural relations better than non-periodic alternatives under held-out languages, families, regions, curation schemes, and an external sparse typological source?**

The project treats the periodic-table idea as a falsifiable historical hypothesis, not a desired visualization.

## Refined Thesis

The confirmatory screen does **not** support a simple global circular/periodic organization of cross-linguistic structural feature relations.

Three findings are currently the most robust:

1. **Directly optimized circular models are repeatedly outpredicted by hierarchical/tree representations under family-held-out evaluation.**
2. **The circular hypothesis also fails direct held-out circularity diagnostics**: a standards-inspired circular-Robinson row-unimodality test and explicit wrap-around closure test do not support a genuine global cycle.
3. **The tree-over-circle ordering replicates qualitatively across TLI, GBI, and WALS**, although the strength and geographic portability of association structure vary substantially by dataset representation.

The safe scientific conclusion is therefore narrower than “language is a tree”:

> **Predictive evidence favors non-circular structure over the tested simple periodic geometry.**

## Dominant Contribution

**An explicit predictive stress test of the historical language-periodic-table hypothesis, using modern global typological data and progressively stricter validation rather than constructing a periodic table by analogy.**

The contribution is not PCA, clustering, topology, typological prediction, or the general observation that genealogy matters; all have substantial prior art.

## Prior-Art Boundary

- **Baker (2001):** periodic-table metaphor and grammatical parameter hierarchy already exist.
- **Port et al. (2018); Port, Karidi & Marcolli (2022):** topology, dimensionality, clustering, and persistent H1 loops in syntactic-parameter spaces already exist.
- **Grambank (2023):** large-scale latent structure, feature bundles, design-space analyses, and strong genealogical effects already exist.
- **Graff et al. (2025):** GBI/TLI dependency-curated structural datasets provide modern substrates.
- **Verkerk et al. (2025/2026):** grammatical universals already receive phylogenetic/spatial testing.
- **SIGTYP/computational typology:** held-out feature prediction is already established.
- **Circular-seriation literature:** circular Robinson structure has formal mathematical definitions; circularity itself is not a method invented here.

The surviving novelty claim remains the **periodic-vs-nonperiodic predictive hypothesis competition plus direct circularity stress tests**.

## Evidence Ladder

### Stage 0 · prerequisite structure

`MIXED_SIGNAL` on TLI.

- 20-component compression: observed 0.510 vs shuffled-null 0.362 (+0.148).
- Pairwise residual association is weak for most pairs but has a substantial upper tail.

Interpretation: enough non-random organization to justify geometry tests; no evidence of periodicity yet.

### Stage 1 · first global model competition

`REFRAME_NONPERIODIC_GEOMETRY`.

On 60 TLI features, family-held-out mean Spearman:

- tree 0.178;
- graph 0.163;
- low-rank / Euclidean 0.150;
- circular 0.109.

The simple circular ordering contained reproducible information but underperformed non-periodic alternatives.

### Stage 1B · fairer circular baseline

`MIXED_ROBUSTNESS`.

The affinity graph was forced connected and one angular coordinate per feature was directly optimized.

- 40 features: optimized circular 0.179; tree 0.178; connected Euclidean 0.217.
- 60 features: optimized circular 0.105; tree 0.147; low-rank 0.153.

The initial circle was not merely an obvious strawman, but its competitiveness was feature-count sensitive.

### Stage 1C · predefined local subsystems

`NO_PREDEFINED_LOCAL_PERIODIC_CANDIDATE`.

Five TLI-defined domains were screened without selecting domains post hoc. None satisfied the predeclared joint requirement of predictive competitiveness and circular-order stability.

The strongest circular-looking subsystem was Grammar linear order: optimized circle 0.401 with order stability 0.811, but tree/low-rank were both ≈0.49. This is evidence for stable ordering, not for a best-in-class cycle.

### Stage 1D · direct circular-Robinson / closure sensitivity

`CIRCULAR_ROBINSON_NOT_SUPPORTED`.

Family-held-out mean row-unimodality violation (lower is better):

- 40 features: circular 0.222, tree 0.209, random 0.237;
- 60 features: circular 0.297, tree 0.284, random 0.307.

Mean circular closure/internal-adjacency ratio:

- 40 features: 0.608;
- 60 features: **0.037**.

The learned circle does not show robust held-out wrap-around closure, which directly weakens the periodic interpretation rather than merely showing that a richer competitor fits better.

### Stage 1E · geographic blocking

`MIXED_GEOGRAPHIC_GENERALIZATION` on TLI.

Under Macroarea or coordinate-cluster hold-outs, all models drop sharply. Circular performance is near zero in the strongest blocks, but non-periodic models also become weak.

This does **not** prove that geography causally destroys a global geometry; it shows that the learned association structure is poorly transportable across large geographic blocks in this representation.

### Stage 1F · repeated family-held-out uncertainty

`TREE_ADVANTAGE_STABLE`.

Across 20/20 TLI family-held-out splits:

- tree: 0.182 ± 0.047;
- circular optimized: 0.109 ± 0.030;
- paired tree − circular mean: **+0.073**;
- 95% bootstrap CI: **[0.055, 0.092]**;
- tree win fraction: **1.00**.

Low-rank also beats circular on average (+0.046; 95% CI [0.033, 0.061]).

### Stage 1G · matched-size calibration of geographic collapse

`GEOGRAPHIC_HETEROGENEITY_CONFIRMED` within TLI.

Matched random test sets rule out test-set size as the simple explanation for the weak geographic transfer:

- Macroarea blocks: geographic train↔test association correlation 0.088 vs matched-random 0.363;
- coordinate clusters: 0.106 vs matched-random 0.351;
- all 10 geographic blocks are below matched-random controls.

However, this result is not promoted to a global conclusion because WALS later behaves differently.

### Stage 1H · GBI alternative-curation replication

`TREE_REPLICATES_OVER_CIRCULAR__WEAK_CROSS_MACROAREA_TRANSFER`.

On 1,140 GBI languages and 60 selected features:

- tree 0.122 ± 0.038;
- circular optimized 0.073 ± 0.036;
- tree − circular = +0.049;
- tree win fraction = 1.00.

Mean cross-Macroarea association transfer = 0.144 ± 0.043.

GBI is an alternative dependency curation, not a fully independent source; it strengthens robustness to curation choice.

### Stage 1I · WALS external sanity replication

`WALS_TREE_OVER_CIRCULAR`.

On 2,659 WALS languages and 30 best-covered parameters:

- tree 0.603 ± 0.026;
- circular optimized 0.410 ± 0.050;
- tree − circular = +0.193;
- tree win fraction = 1.00 across 8 valid family-held-out splits.

But WALS cross-Macroarea association transfer is high: 0.634 ± 0.075. Therefore the strong “geographic collapse” seen in TLI/GBI is **not externally replicated** and must remain a secondary, representation-dependent finding.

## Model-Capacity Interpretation

Tree and graph representations are not exactly capacity-matched to a single circle. Therefore tree > circle is not enough to prove a universal tree geometry.

The negative periodic conclusion is stronger because it also relies on:

- direct optimization of `n-1` angular parameters in the circle;
- predefined-domain tests;
- direct circular-Robinson/closure diagnostics;
- low-rank competitors as well as tree;
- repeated family-held-out uncertainty;
- GBI and WALS qualitative replication.

See `MODEL_CAPACITY_NOTE.md` for the claim boundary.

## Main Hypotheses After Confirmatory Screening

### H1 · Simple global periodic geometry
**Not supported by the current evidence.**

A directly optimized circle fails to provide the best held-out prediction and lacks robust closure / circular-Robinson support.

### H2 · Universal tree geometry
**Not established.**

Tree is a strong predictive benchmark under family hold-out, but its capacity and dataset-dependent geographic portability prevent a claim that language has one universal tree geometry.

### H3 · Structured, non-circular, representation-sensitive design space
**Best current synthesis.**

Cross-linguistic feature relations contain real structure, but a simple global periodic circle is not an adequate universal geometry. Hierarchical/non-circular structure is more predictive under family hold-out, while the portability of the full association geometry depends on data representation and sampling.

## Complexity Intentionally Rejected

- No decorative periodic table as a scientific result.
- No claim that typological features are chemical-like atoms or universal natural kinds.
- No persistent-homology novelty claim.
- No post-hoc torus or multi-cycle model to rescue the original circle; that would be a new preregistered follow-up hypothesis.
- No missing-cell/Mendeleev prediction before a validated generative structure exists.
- No claim that geography itself is the novel result; Grambank already establishes strong genealogical/spatial structure.

## Manuscript Claim Boundary

Allowed wording:

> The global-circle form of the language periodic-table hypothesis tested here is not supported by predictive and held-out circularity evidence; hierarchical/non-circular models provide stronger family-held-out benchmarks across TLI, GBI, and WALS.

Do **not** claim:

- that no possible form of linguistic periodicity can exist;
- that language has been proven to be a tree;
- that TLI/GBI geographic heterogeneity is a universal property of all typological datasets;
- that statistical geometry proves universal grammar or causal mechanisms;
- that family-held-out validation fully removes phylogenetic/contact dependence.

## Promotion Decision

**Scientific screening is now mature enough for formal ARIS secondary review. Do not assign Paper 002 yet.**

The remaining hard gate is identity-bearing secondary review of novelty, model fairness, and manuscript-level claim scope. If that review returns PASS/REVISE without identifying a prior-art collision or fatal design flaw, the candidate can be promoted to the next stable Paper ID with this negative/mixed periodic-hypothesis framing.
