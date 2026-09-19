# Paper 002 · Canonical Handoff

**Paper:** `002-language-geometry`  
**Canonical branch:** `main`  
**Handoff refreshed:** 2026-09-19  
**Observed main SHA at refresh:** `92a6ba22391cc5511e32f68db3f57da56b63a1cd`

This file is the recovery entry point for a new chat, another computer/account, WorkBuddy, Codex, or another agent. For the chronological ChatGPT/agent decision history, see `CHAT_HISTORY.md`. Read repository state before trusting the observed SHA above because ARIS4C is highly concurrent.

## 1. Current state

Paper 002 is **scientifically complete and promoted**.

- idea-stage independent review: PASS / AUTHORIZED;
- manuscript-stage independent WorkBuddy / Tencent Hy3 review: `PASS_SUBMISSION_PREP` / AUTHORIZED;
- no blocking scientific changes;
- no blocking manuscript changes;
- English manuscript: complete;
- Chinese manuscript: complete;
- canonical figures: **6**;
- manuscript-facing tables: **6**;
- current `paper.json` status: `submission-ready-author-metadata-pending`.

The paper must **not** be reopened into new scientific model hunting merely to keep work moving. New model families such as torus/multi-cycle would be new hypotheses and require a new review cycle.

## 2. Frozen scientific claim

Maximum permitted central claim:

> The global-circle form of the language periodic-table hypothesis tested here is not supported by predictive and held-out circularity evidence; hierarchical/non-circular models provide stronger family-held-out benchmarks across TLI, GBI, and WALS, without establishing one universal tree geometry.

Do not broaden this into:
- “language is a tree”;
- “all linguistic periodicity is false”;
- a universal geography claim;
- causal/phylogenetic independence claims.

Important nuance:
- WALS is separately processed but contributes source data to TLI, so Stage 1I is a **representation/sanity robustness check**, not a statistically independent replication.
- Kemp (2026) provides positive circular structure in specific semantic domains; this is compatible with Paper 002's negative result for one global heterogeneous-feature circle.

## 3. Scientific evidence already completed

Do not redo unless a later reviewer finds an actual error.

- Stage 0: non-random compressibility / pairwise association screen.
- Stage 1: null / low-rank / Euclidean / tree / graph / circular model competition.
- Stage 1B: direct angle optimization / circular fairness.
- Stage 1C: predefined local-domain tests.
- Stage 1D: circular-Robinson-style + wrap-around closure diagnostics.
- Stage 1E: geographic / geography+family validation.
- Stage 1F: repeated family hold-out + paired split-bootstrap uncertainty.
- Stage 1G: matched-size geographic calibration.
- Stage 1H: GBI curation/representation robustness.
- Stage 1I: separately processed WALS sanity check.

Core TLI repeated-family result:
- tree Spearman 0.182;
- optimized circle 0.109;
- paired difference +0.073;
- split-bootstrap 95% CI [0.055, 0.092];
- tree wins 20/20 splits.

Cross-representation direction:
- GBI: tree 0.122 > circle 0.073 (12/12);
- WALS: tree 0.603 > circle 0.410 (8/8).

Direct global-circle diagnostic:
- 60-feature closure ratio ≈0.037;
- 40-feature closure ratio 0.608 ± 0.764 is explicitly treated as unstable/non-informative.

## 4. Reviews already passed

### Idea/promotion review
Source:
`../../ideas/language-periodic-system/refine-logs/SECONDARY_REVIEW_RECEIPT.md`

Reviewer:
- WorkBuddy / Tencent Hy3;
- different family from OpenAI GPT primary executor;
- verdict: PASS;
- promotion authorized.

### Manuscript-stage review
Source:
`MANUSCRIPT_REVIEW_RECEIPT.md`

Verdict:
- `PASS_SUBMISSION_PREP`;
- submission-prep authorization: AUTHORIZED;
- no blocking scientific changes;
- no blocking manuscript changes.

Optional reviewer suggestions already implemented:
- narrower title: “predictive evidence does not support a global circular organization”;
- Stage-1 0.35 vs Stage-1C 0.40 stability thresholds clarified in code;
- 40-feature closure-ratio instability made explicit.

## 5. Canonical manuscripts and outputs

Read:

1. `../paper.json`
2. `STATUS.md`
3. `../manuscript/DRAFT.md`
4. `../manuscript/DRAFT.zh-CN.md`
5. `../manuscript/TABLES.md`
6. `CLAIMS_EVIDENCE_MATRIX.md`
7. `DATA_PROVENANCE.md`
8. `MANUSCRIPT_REVIEW_RECEIPT.md`

Current canonical delivery:
- English paper: complete;
- Chinese paper: complete;
- figures: 6;
- tables: 6;
- public English/Chinese HTML/PDF outputs recorded in `paper.json`.

## 6. Submission target

Primary target:
**Linguistic Typology**

Backup:
**Journal of Language Evolution**

Why LT first:
the manuscript is typology-first (cross-linguistic variation, structural feature organization, limits on diversity, typological method) rather than primarily an evolutionary-process paper.

Submission package root:
`../submission/linguistic-typology/`

## 7. Critical submission-package state

**Do not mistake the old technical PASS for the current six-figure package.**

Historical technical QA:
- workflow run: `35412714647`;
- artifact: `10575195098`;
- build commit: `608bc871fd4a634a0906b93aeabcd47675e8cb08`;
- verdict: `TECHNICAL_SUBMISSION_PACKAGE_PASS`;
- 31-page blinded DOCX/PDF;
- full visual QA;
- anonymisation clean;
- Table 6 page-break fixed.

However, that reviewed artifact contained **3 figures**.

After that QA, the canonical EN/ZH manuscripts were expanded to **6 figures**. Therefore:

> **The current hard technical task is to rebuild and re-QA the Linguistic Typology package against the canonical six-figure manuscript.**

The old artifact remains useful historical provenance but must not be uploaded to ScholarOne as the final package.

See:
`../submission/linguistic-typology/SUBMISSION_QA.md`

## 8. Current next steps — exact order

1. Refresh `submission/linguistic-typology/MANUSCRIPT_BLINDED.md` so it matches the canonical six-figure English manuscript.
2. Refresh submission figure files / legends / alt text from the canonical six figures.
3. Re-run `.github/workflows/paper002-build-submission.yml`.
4. Confirm the new build succeeds.
5. Download the **new** artifact, not historical artifact 10575195098.
6. Re-run:
   - DOCX/PDF page-by-page visual QA;
   - table clipping / figure legibility checks;
   - DOCX↔PDF text parity;
   - author-identity scan in blinded manuscript;
   - supplement anonymisation scan;
   - metadata/creator scan.
7. Update `submission/linguistic-typology/SUBMISSION_QA.md` with the new six-figure build run/artifact/digest and change the scope warning to a current PASS only if QA genuinely passes.
8. Update `paper.json`:
   - set `package_refresh_required=false`;
   - remove the package-refresh blocking item;
   - record the new verified workflow run/artifact.
9. Only then request/fill the author's human-only metadata.
10. ScholarOne upload/submit is the final external action.

## 9. Human-only metadata still required

Do not invent these.

- IPA transcription of author name;
- department;
- institution;
- street address;
- city;
- postal code;
- country;
- institutional/corresponding email;
- ORCID or none;
- funding statement;
- conflict-of-interest statement;
- confirm CRediT roles;
- confirm originality / not under consideration elsewhere.

The title page, cover letter and declarations templates already contain placeholders.

## 10. Reproducibility / submission infrastructure

Existing workflows:
- `.github/workflows/paper002-manuscript.yml`
- `.github/workflows/paper002-supplement.yml`
- `.github/workflows/paper002-build-submission.yml`
- `.github/workflows/paper002-env-freeze.yml`

Frozen contemporary environment:
- Python 3.12.14
- NumPy 2.5.3
- pandas 3.0.6
- SciPy 1.18.1
- scikit-learn 1.9.1
- matplotlib 3.11.2

Historical submission QA verified no identity leakage for:
- CochraneK;
- Cochrane Kang;
- WorkBuddy;
- Tencent;
- ARIS4C.

Repeat this after six-figure rebuild.

## 11. Important implementation / reporting corrections already made

Do not regress these:

- Stage 0 is mode imputation → one-hot → **TruncatedSVD**, not ordinary PCA.
- Stage-0 NMI is pairwise NMI with within-pair permutation null, not “residual NMI”.
- GBI: ≥180 observations, 2–15 states, top 60 by coverage/lower-cardinality; 12 family splits.
- TLI/GBI family metadata use Glottolog; WALS uses its CLDF family/macroarea fields.
- WALS source overlap with TLI is explicit.
- Stage 1–1I are exploratory/screening, not one preregistered confirmatory family.
- Split-bootstrap intervals quantify split sensitivity, not phylogenetic uncertainty.
- Geography result is representation-dependent; WALS contradicts TLI/GBI on cross-macroarea transfer.

## 12. Literature boundary

Latest dedicated collision rescan on record:
2026-09-18.

Important additions:
- Kemp (2026), domain-specific circular category systems;
- Evangelopoulos et al. (2020), general circular arrangement / embedding method prior art.

Rescan verdict:
`NO_NEW_FATAL_COLLISION_FOUND`.

Do not claim novelty for:
- clustering languages;
- TDA/persistent homology on syntax;
- generic held-out typological prediction;
- generic circular seriation;
- “genealogy matters”.

The novelty wedge remains the explicit held-out stress test of a **simple global circular/periodic structural-feature geometry** against non-periodic alternatives, with direct closure/circularity diagnostics and cross-representation robustness.

## 13. ARIS4C concurrency warning

ARIS4C is actively modified by many parallel chats/agents. Before writing:
- fetch latest `main`;
- fetch the exact target file SHA;
- avoid assuming a previously observed main SHA is current;
- do not overwrite Paper 002 files with stale 3-figure versions;
- prefer targeted file updates over broad branch replay when main has moved substantially.

## 14. Safe restart prompt

A future agent can be told:

> Continue ARIS4C Paper 002 from `papers/002-language-geometry/process/HANDOFF.md`. Read current Git `main` first. Do not redo science or reviews. The current task is the six-figure Linguistic Typology submission-package refresh and technical QA, followed by author metadata and ScholarOne submission.

