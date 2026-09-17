# Research Brief · Language Periodic System

> ARIS4C active candidate. Intended input to ARIS `/idea-discovery` or `/research-pipeline` from this candidate directory.

## Problem Statement

The metaphor of a “periodic table of languages” is old: Baker (2001) explicitly proposed organizing grammatical parameters into a systematic table. Modern cross-linguistic databases now make a stronger question testable: **does structural language diversity actually have a recurrent geometry that deserves the word periodic, or is the metaphor misleading?**

The paper should not construct a visually appealing table and then rationalize it. It should operationalize periodicity, compare it against plausible alternatives, and let out-of-sample evidence decide. The scientific target is therefore model selection over the geometry of cross-linguistic structural space.

A successful result may be positive (a periodic/circular/toroidal organization adds reproducible predictive value), local (periodicity exists only within particular structural modules), or negative (tree/graph/manifold/factor models dominate). The contribution is the falsifiable test and the resulting characterization of language design space.

## Background

- **Field:** linguistic typology / computational typology / quantitative linguistics
- **Sub-area:** cross-linguistic structural feature geometry and dependency
- **Key prior work:**
  - Baker (2001), *The Atoms of Language*, chapter “Toward a Periodic Table of Languages”. Establishes that the broad metaphor and parameter-atom framing are not novel.
  - Port et al. (2018), *Persistent Topology of Syntax*. Uses persistent homology on syntactic-parameter data and finds family-specific non-trivial topology.
  - Port, Karidi & Marcolli (2022), *Topological Analysis of Syntactic Structures*. Studies dimensionality, hierarchical clustering, and persistent H1 loops in SSWL/LanGeLin data. This means “apply TDA and find loops” is not novel.
  - Skirgård et al. (2023), Grambank. Large-scale morphosyntactic database; PCA/feature-bundle/latent-class analyses constrain claims of a tiny global parameter system.
  - Graff et al. (2025), GBI/TLI. Curates structural features to reduce logical and strong statistical dependencies; TLI spans grammar, phonology, and colexification.
  - Verkerk et al. (2025/2026), *Enduring constraints on grammar...*. Tests 191 proposed universals with phylogenetic and spatial controls; supports a minority but demonstrates recurrent constraints.
  - SIGTYP 2020 and follow-up computational typology work. Typological feature prediction is established; prediction alone is not novel.
- **What we already tried:** Stage-0 prerequisite screen on TLI-statistical densified-small.
- **What did not work / claims ruled out:** novelty cannot rest on the phrases “periodic table of language”, “linguistic atoms”, ordinary clustering, ordinary typological feature prediction, or persistent-homology loops.

## Constraints

- **Compute:** CPU-first preferred; no GPU should be required for the core paper. Moderate bootstrap/model-comparison workloads are acceptable.
- **Data:** prioritize open, citable datasets. Primary candidate: curated TLI/GBI; use Glottolog for genealogical metadata and available coordinates for areal controls. Grambank can be a replication dataset.
- **Timeline:** exploratory now; no fixed submission deadline.
- **Target venue:** undecided. Likely quantitative/computational linguistics or language-evolution venue if the method survives validation.
- **Reproducibility:** every claim should be generated from versioned code and machine-readable outputs in ARIS4C.

## What We Are Looking For

- [x] Diagnostic / analysis paper
- [x] Explicit competing-model comparison
- [x] A falsifiable formalization of “periodic system”
- [x] Out-of-sample prediction rather than descriptive fit alone
- [ ] A predetermined periodic table visualization

## Domain Knowledge / Working Hypotheses

### H0 · No special recurrent geometry
Once feature construction, missingness, genealogy, and geography are controlled, periodic models do not outperform simpler alternatives.

### H1 · Global periodic organization
A low-dimensional periodic geometry (circle/torus/lattice-like recurrence) yields reproducible held-out predictive advantage over Euclidean factor, hierarchy/tree, graph/manifold, and null alternatives.

### H2 · Local periodicity
No single global periodic system exists, but stable periodic/recurrent geometry appears within one or more independently defined structural modules and generalizes across families/regions.

A claim of periodicity must require more than an H1 loop in persistent homology. At minimum it should imply a stable recurrent ordering/topology plus out-of-sample predictive value that cannot be reproduced by non-periodic competitors with comparable capacity.

## Non-Goals

- Do not claim to invent the language-periodic-table metaphor.
- Do not equate a PCA plot, clustering, UMAP/t-SNE shape, or persistent loop with periodicity.
- Do not select only examples that visually fit a cycle.
- Do not treat language-family inheritance or geographic diffusion as a universal structural law.
- Do not force the final narrative to be positive; a well-powered rejection of the periodic hypothesis is acceptable.
- Do not assign a stable Paper ID until the novelty and Stage-1 discrimination tests survive review.

## Existing Results

Stage-0 on 644 languages from the statistically curated TLI densified-small dataset found `MIXED_SIGNAL`:

- 120-feature PCA compression: 20 observed components explained 0.510 of variance vs 0.362 under a feature-wise marginal-preserving shuffle null (difference +0.148).
- Residual pairwise association across 3,143 tested pairs: observed NMI median 0.007 vs null 0.003; p90 0.037 vs 0.016; p99 0.119 vs 0.039.

Interpretation: cross-linguistic structure is substantially more compressible than an independence-style null, with a tail of strong residual associations, but this is **not evidence of periodicity**. It is enough to justify a discriminating Stage-1 model comparison.

## Promotion Gate

Promote to a numbered ARIS4C paper only if all of the following hold:

1. the closest-prior-work review still leaves a defensible gap after Port/Marcolli, Grambank, and computational typology work;
2. periodicity receives a precise capacity-controlled definition;
3. at least one held-out evaluation can distinguish periodic from non-periodic alternatives;
4. genealogy/geography are handled explicitly in confirmatory analyses;
5. an independent ARIS reviewer returns a positive identity-bearing verdict or a clearly documented revised route survives review.
