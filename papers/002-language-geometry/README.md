# Paper 002 · Testing the Periodic-Table Hypothesis of Human Language

**Status:** scientific manuscript complete · independent manuscript review `PASS_SUBMISSION_PREP` · bilingual six-figure public output complete · Linguistic Typology package refresh + author metadata/declarations pending  
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
- WALS separately processed sparse sanity check: tree 0.603 vs circle 0.410.
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

Draft v1 implements all manuscript-level boundaries required by the independent Hy3 secondary review. The independent **manuscript-stage** review is complete with `PASS_SUBMISSION_PREP`. A Linguistic Typology technical package also passed QA at build commit `608bc871fd4a634a0906b93aeabcd47675e8cb08`; that historical QA covered a three-figure package. The canonical manuscript was later expanded to six figures, so the journal package must be rebuilt and re-QA'd before submission. No further scientific expansion is required for Paper 002.


## Bilingual manuscript

- English canonical manuscript: `manuscript/DRAFT.md`
- Chinese complete version: `manuscript/DRAFT.zh-CN.md`

The Chinese version preserves the same numerical results, claim boundaries, and limitations as the independently reviewed English manuscript. It is an ARIS4C bilingual-delivery artifact; the journal submission remains the blinded English package under `submission/linguistic-typology/`.


## Current finalization state

Paper 002 is scientifically complete and the repository-level output gate is complete. Before journal submission, one editorial synchronization step remains because the canonical manuscript was expanded from three to six figures after the last technical submission-package QA:

- rebuild the Linguistic Typology package from the current six-figure manuscript and repeat technical/visual QA;
- confirm author identity/contact metadata required by the journal;
- confirm funding, conflict-of-interest, CRediT and originality declarations;
- copy the confirmed metadata into ScholarOne and perform the actual submission.

Canonical details are in `submission/linguistic-typology/SUBMISSION_METADATA_CHECKLIST.md` and `SUBMISSION_QA.md`. The manuscript claim remains scientifically frozen; new model families or post-hoc hypothesis expansion belong in a new paper rather than being appended to Paper 002.
