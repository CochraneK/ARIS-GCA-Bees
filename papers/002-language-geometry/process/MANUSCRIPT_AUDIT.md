# Paper 002 · Manuscript Draft v1 Adversarial Audit

**Audit type:** primary-executor advisory self-audit  
**Independence:** NOT an ARIS secondary review; same model family as primary executor  
**Scope:** Draft v1 claim discipline, numerical consistency, reviewer-requirement coverage

## Result

**No blocking claim-boundary violation found.**

Draft v1 is suitable for integration into `main` as a manuscript-stage artifact, not as a submission-ready final paper.

## Checks performed

### 1. Reviewer-mandated boundaries

PASS in Draft v1:

- bootstrap is explicitly described as split-sensitivity uncertainty, not phylogenetic uncertainty;
- residual genealogy/contact dependence remains an explicit limitation;
- Stage 1–1I are labeled exploratory/screening and adaptive;
- WALS vs TLI/GBI geographic-transfer contradiction is preserved;
- Baker's metaphor is not equated with a literal circle;
- claim is restricted to the tested **simple global circle**;
- tree superiority is not translated into “language is a tree”;
- major N, feature counts, selection rules and effect sizes are reported.

### 2. Numerical cross-check

Core manuscript numbers were cross-checked against source reports:

- Stage 0: 20-component 0.510 vs null 0.362; p99 residual NMI 0.119 vs 0.039.
- Stage 1: family-held-out tree 0.178, graph 0.163, low-rank 0.150, circle 0.109.
- Stage 1B: 40-feature circle 0.179/tree 0.178; 60-feature circle 0.105/tree 0.147/low-rank 0.153.
- Stage 1C: Grammar linear order circle 0.401, stability 0.811, tree 0.494.
- Stage 1D: 60-feature circular violation 0.297 vs tree 0.284; closure ratio 0.037.
- Stage 1F: tree 0.182 vs circle 0.109; paired +0.073; CI [0.055, 0.092].
- Stage 1G: TLI macroarea 0.088 vs matched-random 0.363; clusters 0.106 vs 0.351.
- Stage 1H: GBI tree 0.122 vs circle 0.073; macroarea transfer 0.144.
- Stage 1I: WALS tree 0.603 vs circle 0.410; macroarea transfer 0.634.

### 3. Model-description cross-check

Verified against implementation:

- NMI uses arithmetic normalization.
- main TLI feature eligibility: ≥180 observed values, 2–15 states, then coverage/lower-cardinality ranking.
- tree = average linkage on (1-NMI), cophenetic distance, quadratic calibration.
- graph = 6-nearest-neighbor weighted graph + shortest-path distance + quadratic calibration.
- optimized circle = (n-1) free angular coordinates, first feature fixed at zero, two cosine harmonics, L-BFGS-B training-MSE optimization.
- held-out test associations are not used in model fitting.

### 4. Known remaining weaknesses

Not blockers for Draft v1, but required before submission:

1. run the figure-generation script in a clean environment and commit regenerated SVGs;
2. pin future numerical reruns to immutable upstream data URLs + input checksums;
3. freeze dependency versions;
4. perform a manuscript-stage independent cross-family review;
5. verify formatted bibliography metadata one final time;
6. consider whether 50–100 family splits or a phylogenetic sensitivity supplement is worth the cost before journal submission.

## Claim lock

The following remains the maximum central claim for Draft v1:

> The global-circle form of the language periodic-table hypothesis tested here is not supported by predictive and held-out circularity evidence; hierarchical/non-circular models provide stronger family-held-out benchmarks across TLI, GBI, and WALS, without establishing one universal tree geometry.
