# Paper 002 · Testing the Periodic-Table Hypothesis of Human Language

**Status:** manuscript Draft v1 complete · independent manuscript-stage review pending  
**Canonical paper ID:** `002`  
**Slug:** `language-geometry`

## Central claim

> The global-circle form of the language periodic-table hypothesis tested here is not supported by predictive and held-out circularity evidence; hierarchical/non-circular models provide stronger family-held-out benchmarks across TLI, GBI, and WALS, without establishing one universal tree geometry.

## Promotion record

This paper was developed first as the staging candidate:

`ideas/language-periodic-system/`

It was promoted to formal Paper 002 after an independent WorkBuddy review using **Tencent Hy3**, a different model family from the OpenAI GPT primary executor. WorkBuddy returned:

- verdict: **PASS**
- promotion authorization: **AUTHORIZED**
- no fatal prior-art collision
- manuscript-stage mandatory claim/clarity requirements, but no blocking additional experiment

The full exploratory and robustness-screening history remains in `ideas/language-periodic-system/` as provenance rather than being deleted or rewritten.

## Key evidence

- TLI repeated family-held-out: tree 0.182 vs optimized circle 0.109; paired difference +0.073, bootstrap 95% CI [0.055, 0.092], tree wins 20/20.
- Direct circular-Robinson / closure diagnostics do not support a robust global cycle; 60-feature wrap-around closure ratio ≈0.037.
- No predefined TLI structural domain met the joint predictive + stability threshold for local periodicity.
- GBI replication: tree 0.122 vs circle 0.073.
- WALS external sanity replication: tree 0.603 vs circle 0.410.
- Geographic portability is representation-dependent and must not be promoted to a universal claim.

## Review-imposed manuscript requirements

The manuscript must:

1. state that bootstrap uncertainty measures split sensitivity, not phylogenetic uncertainty;
2. state that residual genealogical/contact dependence is not fully removed;
3. describe Stage 1–1I as exploratory/screening rather than preregistered confirmation;
4. preserve the WALS vs TLI/GBI geography contradiction;
5. state clearly that the test targets the **simple global circle** form, not every conceivable periodic or Baker-style parameter system;
6. report per-stage N, feature set, feature-selection rule, effect sizes, and uncertainty.

See `process/SECONDARY_REVIEW_RECEIPT.md` and `process/STATUS.md`.

## Provenance

The staging directory remains canonical for the full analysis code/results generated before promotion:

`../../ideas/language-periodic-system/`

Future manuscript-facing artifacts should be developed inside this Paper 002 directory.


## Manuscript v1

- Main draft: `manuscript/DRAFT.md`
- Core result tables: `manuscript/TABLES.md`
- Figure captions: `manuscript/FIGURE_CAPTIONS.md`
- Figures: `figures/`
- Claims–evidence matrix: `process/CLAIMS_EVIDENCE_MATRIX.md`
- Data provenance: `process/DATA_PROVENANCE.md`
- Draft audit: `process/MANUSCRIPT_AUDIT.md`

Draft v1 implements all manuscript-level boundaries required by the independent Hy3 secondary review. The next hard quality gate is an independent **manuscript-stage** review, not another idea-stage promotion review.
