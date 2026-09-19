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
- [x] Annotate Stage-1D closure-ratio interpretation.
- [ ] Consider permutation/p-value supplement.

Reviewer-listed non-scientific cleanups already closed: the title uses the narrower “does not support a global circular organization” wording; the Stage-1 0.35 vs Stage-1C 0.40 threshold distinction is commented in source; and the 40-feature closure-ratio SD is explicitly described as unstable/non-informative in the manuscript.

## Provenance

Full pre-promotion evidence/code remains under:

`../../ideas/language-periodic-system/`

Secondary review source:

`../../ideas/language-periodic-system/refine-logs/SECONDARY_REVIEW_RECEIPT.md`


## Draft v1 artifacts

- `../manuscript/DRAFT.md`
- `../manuscript/TABLES.md`
- `../manuscript/FIGURE_CAPTIONS.md`
- `../figures/figure1_local_domain_gate.svg`
- `../figures/figure2_circular_diagnostics.svg`
- `../figures/figure3_tli_paired_contrasts.svg`
- `../figures/figure4_geography_calibration.svg`
- `../figures/figure5_cross_dataset.svg`
- `../figures/figure6_stable_order_not_closure.svg`
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
- [x] GitHub Actions manuscript CI checks manifest/artifacts/claim boundaries and verifies both EN/ZH manuscripts reference the six canonical figures in order. The legacy three-plot generator is retained as a source-data smoke test but is not the complete six-figure renderer.
- [x] Latest `main` Paper 002 manuscript CI: SUCCESS.
- [x] Stale concurrency PRs #9 and #11 closed after safe direct integration.

## Current hard gate

**Different-family manuscript-stage review: COMPLETE (PASS_SUBMISSION_PREP).**

- Reviewer: WorkBuddy / hy3 (non-OpenAI-GPT; different model family from the OpenAI GPT primary manuscript writer).
- Receipt: `MANUSCRIPT_REVIEW_RECEIPT.md` (verdict `PASS_SUBMISSION_PREP`; `Submission-prep authorization: AUTHORIZED`).
- No blocking scientific or manuscript changes. Optional improvements only (title tightening; `stage1.py:414` 0.35 vs Stage 1C 0.40 code comment; 40-feature closure-ratio SD note; optional 50–100 splits / phylogenetic sensitivity).

### Next step

~~**Target-journal formatting / submission preparation (editorial only).**~~ **COMPLETE (2026-09-19).** The Linguistic Typology technical package passed final QA. The maximum permitted claim remains frozen at the bounded wording in §Scientific freeze and must not be broadened without a new review cycle. Any new substantive model family (e.g. torus/multi-cycle) is a new hypothesis and should not be introduced post hoc into Paper 002.

**Current remaining gate:** refresh/rebuild the Linguistic Typology submission package against the canonical six-figure manuscript, re-run technical QA, then supply author metadata/declarations and perform the ScholarOne upload/submit.


## Submission-package gate · 2026-09-19

**State:** HISTORICAL TECHNICAL PACKAGE PASS · SIX-FIGURE REFRESH REQUIRED

Primary target: **Linguistic Typology**

Completed:
- independent manuscript review: `PASS_SUBMISSION_PREP`;
- journal-specific blinded manuscript formatting;
- 160-word abstract + 5 keywords;
- six in-manuscript tables;
- historical reviewed build contained three in-manuscript and separately uploadable figures; canonical EN/ZH manuscripts were subsequently expanded to six figures;
- title-page / cover-letter / declarations templates;
- anonymised Stage 0–1I supplement;
- pinned contemporary reproduction environment;
- supplement CI;
- DOCX/PDF generation workflow;
- full 31-page final visual QA;
- anonymisation scans;
- final artifact provenance recorded in `submission/linguistic-typology/SUBMISSION_QA.md`.

**Remaining hard gate:** rebuild/re-QA the journal package so it matches the six-figure canonical manuscript; then author-supplied submission metadata and explicit declarations, followed by ScholarOne upload/submit.

No additional scientific analysis is currently required. The package refresh is editorial/reproducibility work caused by post-QA visual expansion, not a reopening of the scientific claim.


## Bilingual delivery

**State:** COMPLETE

- English canonical manuscript: `../manuscript/DRAFT.md`
- Chinese complete manuscript: `../manuscript/DRAFT.zh-CN.md`
- figures: 6
- manuscript-facing tables: 6
- output gate metadata: PASS-ready in `../paper.json`

The Chinese manuscript preserves the same numerical results and bounded claim as the independently reviewed English manuscript. It is a portfolio/delivery artifact and does not alter the blinded English journal-submission package.


## 2026-09-19 continuity checkpoint

- Canonical English and Chinese manuscripts each contain the same ordered six-figure narrative.
- Latest known Paper 002 manuscript CI covering the six-figure repository state before this checkpoint: run #114 (`35422718503`) on commit `99568d00fa33b6dd8bae7610965d32d5bac213c2`, conclusion **success**.
- The older Linguistic Typology technical QA remains valid only for build commit `608bc871fd4a634a0906b93aeabcd47675e8cb08`, which packaged three figures. Do not interpret that historical PASS as QA of the current six-figure submission package.
- Scientific claim remains frozen; torus/multi-cycle/multi-level/local follow-up hypotheses belong in a new paper rather than post-hoc expansion of Paper 002.
