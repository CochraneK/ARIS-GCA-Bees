# Paper 002 Status

**Paper:** `002-language-geometry`  
**Stage:** manuscript Draft v1 complete · independent manuscript review PASS_SUBMISSION_PREP  
**Promotion gate:** PASSED  
**Secondary reviewer:** WorkBuddy / Tencent Hy3  
**Reviewer family:** Tencent Hunyuan (different from OpenAI GPT primary executor)  
**Verdict:** PASS  
**Promotion authorization:** AUTHORIZED

## Scientific freeze

Permitted central claim:

> The global-circle form of the language periodic-table hypothesis tested here is not supported by predictive and held-out circularity evidence; hierarchical/non-circular models provide stronger family-held-out benchmarks across TLI, GBI, and WALS, without establishing one universal tree geometry.

This wording may be narrowed during manuscript review but must not be broadened beyond the secondary-review boundaries without a new review cycle.

## Mandatory manuscript tasks

- [x] Clarify bootstrap = split-sensitivity uncertainty, not phylogenetic uncertainty.
- [x] Explicitly retain residual genealogical/contact dependence as a limitation.
- [x] Label Stage 1–1I exploratory/screening and discuss multiplicity.
- [x] Preserve WALS vs TLI/GBI geographic-transfer contradiction.
- [x] Scope the hypothesis to the simple global-circle form.
- [x] Report N, feature selection, effect sizes and CIs stage by stage.

## Optional robustness

- [ ] Increase family-held-out splits to 50–100.
- [ ] Consider phylogenetic/spatiophylogenetic sensitivity model.
- [ ] Annotate Stage-1D closure-ratio interpretation.
- [ ] Consider permutation/p-value supplement.

## Provenance

Full pre-promotion evidence/code remains under:

`../../ideas/language-periodic-system/`

Secondary review source:

`../../ideas/language-periodic-system/refine-logs/SECONDARY_REVIEW_RECEIPT.md`


## Draft v1 artifacts

- `../manuscript/DRAFT.md`
- `../manuscript/TABLES.md`
- `../manuscript/FIGURE_CAPTIONS.md`
- `../figures/figure1_cross_dataset.svg`
- `../figures/figure2_tli_paired_contrasts.svg`
- `../figures/figure3_circular_diagnostics.svg`
- `DATA_PROVENANCE.md`
- `CLAIMS_EVIDENCE_MATRIX.md`
- `MANUSCRIPT_AUDIT.md`

## Next hard gate

~~Obtain a fresh, different-family **manuscript-stage review** of Draft v1. This is a quality gate for wording/method reporting/submission readiness; Paper 002 itself is already formally promoted.~~

**COMPLETE (2026-09-18):** different-family manuscript-stage review returned `PASS_SUBMISSION_PREP`; `MANUSCRIPT_REVIEW_RECEIPT.md` + `.json` written. No blocking scientific or manuscript changes. Optional improvements only (title tightening; 0.35/0.40 code comment; 40-feature closure-ratio SD note; optional 50–100 splits / phylogenetic sensitivity).


## Independent manuscript-review handoff

Prepared:
- `WORKBUDDY_MANUSCRIPT_REVIEW.md`
- `MANUSCRIPT_REVIEW_RECEIPT.template.json`

A fresh different-family reviewer wrote `MANUSCRIPT_REVIEW_RECEIPT.md`. Verdict `PASS_SUBMISSION_PREP` authorizes target-journal formatting; `REOPEN_ANALYSIS` would reopen scientific work (not required).


## Pre-review hardening · 2026-09-18

**State:** COMPLETE

- [x] Draft v1 complete.
- [x] Independent idea-stage secondary review PASS retained.
- [x] 2026 literature collision rescan completed; no new fatal collision found.
- [x] Kemp (2026) domain-specific circular/symmetry work integrated and distinguished from global feature-space circularity.
- [x] General circular-seriation method prior art expanded.
- [x] Core bibliography metadata audited.
- [x] Stage 0 terminology aligned to implementation (mode imputation + one-hot + TruncatedSVD; pairwise NMI permutation null).
- [x] WALS–TLI source overlap made explicit; Stage 1I no longer described as an independent replication.
- [x] TLI/GBI vs WALS family-metadata code paths documented accurately.
- [x] GBI feature-selection and 12-split rules documented.
- [x] Stage inventory table added.
- [x] Clean GitHub Actions manuscript CI regenerates all three figures and checks manifest/artifacts/claim boundaries.
- [x] Latest `main` Paper 002 manuscript CI: SUCCESS.
- [x] Stale concurrency PRs #9 and #11 closed after safe direct integration.

## Current hard gate

**Different-family manuscript-stage review: COMPLETE (PASS_SUBMISSION_PREP).**

- Reviewer: WorkBuddy / hy3 (non-OpenAI-GPT; different model family from the OpenAI GPT primary manuscript writer).
- Receipt: `MANUSCRIPT_REVIEW_RECEIPT.md` (verdict `PASS_SUBMISSION_PREP`; `Submission-prep authorization: AUTHORIZED`).
- No blocking scientific or manuscript changes. Optional improvements only (title tightening; `stage1.py:414` 0.35 vs Stage 1C 0.40 code comment; 40-feature closure-ratio SD note; optional 50–100 splits / phylogenetic sensitivity).

### Next step

**Target-journal formatting / submission preparation (editorial only).** The maximum permitted claim is frozen at the bounded wording in §Scientific freeze; it may be narrowed during formatting but not broadened without a new review cycle. No further primary-executor scientific expansion should be added merely to keep the project moving. Any new substantive model family (e.g. torus/multi-cycle) is a new hypothesis and should not be introduced post hoc into Paper 002.


## Submission-package gate · 2026-09-19

**State:** TECHNICAL PACKAGE COMPLETE

Primary target: **Linguistic Typology**

Completed:
- independent manuscript review: `PASS_SUBMISSION_PREP`;
- journal-specific blinded manuscript formatting;
- 160-word abstract + 5 keywords;
- six in-manuscript tables;
- three in-manuscript and separately uploadable figures;
- title-page / cover-letter / declarations templates;
- anonymised Stage 0–1I supplement;
- pinned contemporary reproduction environment;
- supplement CI;
- DOCX/PDF generation workflow;
- full 31-page final visual QA;
- anonymisation scans;
- final artifact provenance recorded in `submission/linguistic-typology/SUBMISSION_QA.md`.

**Remaining hard gate:** author-supplied submission metadata and explicit declarations, followed by ScholarOne upload/submit.

No additional scientific analysis or manuscript expansion is currently required.
