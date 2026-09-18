# Paper 002 Status

**Paper:** `002-language-geometry`  
**Stage:** manuscript Draft v1 complete · independent manuscript review pending  
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

Obtain a fresh, different-family **manuscript-stage review** of Draft v1. This is a quality gate for wording/method reporting/submission readiness; Paper 002 itself is already formally promoted.


## Independent manuscript-review handoff

Prepared:
- `WORKBUDDY_MANUSCRIPT_REVIEW.md`
- `MANUSCRIPT_REVIEW_RECEIPT.template.json`

A fresh different-family reviewer should write `MANUSCRIPT_REVIEW_RECEIPT.md`. A `PASS_SUBMISSION_PREP` verdict authorizes target-journal formatting; `REOPEN_ANALYSIS` reopens scientific work.


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

**Different-family manuscript-stage review.**

Use:
`WORKBUDDY_MANUSCRIPT_REVIEW.md`

Expected output:
`MANUSCRIPT_REVIEW_RECEIPT.md`

Possible verdicts:
- `PASS_SUBMISSION_PREP`
- `REVISE_MANUSCRIPT`
- `REOPEN_ANALYSIS`
- `STOP_MANUSCRIPT`

No further primary-executor scientific expansion should be added merely to keep the project moving before this independent review. Any new substantive model family (e.g. torus/multi-cycle) is a new hypothesis and should not be introduced post hoc into Paper 002.
