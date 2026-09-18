# WorkBuddy Handoff · Paper 002 Manuscript-Stage Review

**Paper:** `002-language-geometry`  
**Canonical branch:** `main`  
**Primary manuscript writer family:** OpenAI GPT / ChatGPT  
**Required reviewer:** fresh session, different model family  
**Review type:** manuscript quality / submission-readiness review  
**This is NOT the idea-stage promotion gate:** Paper 002 is already formally promoted.

## Entry point

Read in this order:

1. `papers/002-language-geometry/manuscript/DRAFT.md`
2. `papers/002-language-geometry/manuscript/TABLES.md`
3. `papers/002-language-geometry/manuscript/FIGURE_CAPTIONS.md`
4. `papers/002-language-geometry/process/CLAIMS_EVIDENCE_MATRIX.md`
5. `papers/002-language-geometry/process/REVIEW_REQUIREMENTS.md`
6. `papers/002-language-geometry/process/DATA_PROVENANCE.md`
7. `papers/002-language-geometry/process/MANUSCRIPT_AUDIT.md`
8. `papers/002-language-geometry/process/LITERATURE_RESCAN_2026-09-18.md`
9. `papers/002-language-geometry/process/SECONDARY_REVIEW_RECEIPT.md`

For any important numerical claim, inspect the source report / JSON under:

`ideas/language-periodic-system/`

For any important implementation claim, inspect the relevant `stage1*.py`.

## Reviewer mission

Try to make the manuscript fail.

Review independently rather than polishing toward agreement. Search the literature again through the review date.

Evaluate:

1. title/abstract fidelity;
2. novelty wording relative to Baker, Port/Marcolli, Grambank, Graff GBI/TLI, Verkerk, SIGTYP, Kemp (2026) symmetry/circular category systems, and circular-seriation work;
3. whether the single-global-circle operationalization is described fairly rather than presented as Baker's literal model;
4. exact consistency between Methods and implementation;
5. exact consistency between Results/Tables/Figures and archived JSON;
6. whether exploratory Stage 1–1I multiplicity is sufficiently disclosed;
7. whether split-bootstrap uncertainty is correctly bounded;
8. whether genealogy/contact limitations are sufficiently visible;
9. whether tree/model-capacity limitations prevent overclaim;
10. whether the WALS-vs-TLI/GBI geography contradiction is preserved;
11. whether figures/captions can be misread as cross-dataset effect-size comparisons;
12. whether any unsupported causal, universal, “language is a tree”, or “all periodicity is disproven” wording appears;
13. whether the manuscript is coherent enough for journal formatting without another scientific analysis.

## Decision

Return one of:

- `PASS_SUBMISSION_PREP` — scientific manuscript can proceed to target-journal formatting; only editorial/formatting work remains.
- `REVISE_MANUSCRIPT` — central paper remains viable but mandatory manuscript changes are required.
- `REOPEN_ANALYSIS` — at least one manuscript problem cannot be repaired without new analysis.
- `STOP_MANUSCRIPT` — fatal novelty/method/validity problem makes this paper framing non-viable.

## Mandatory distinction

Separate:

- **blocking scientific changes**
- **blocking manuscript changes**
- **optional improvements**

Do not turn optional 50–100 splits or a full phylogenetic model into a blocker unless your independent review identifies a concrete reason the present bounded claim is invalid without them.

## Required receipt

Create:

`papers/002-language-geometry/process/MANUSCRIPT_REVIEW_RECEIPT.md`

with:

```markdown
# Paper 002 Manuscript Review Receipt

## Reviewer identity
- provider/app:
- exact model:
- model family:
- independent from primary manuscript writer: YES / NO
- fresh session: YES / NO
- trace/session ID:
- timestamp:
- literature search cutoff:

## Verdict
PASS_SUBMISSION_PREP / REVISE_MANUSCRIPT / REOPEN_ANALYSIS / STOP_MANUSCRIPT

## Executive assessment
...

## Novelty and literature
...

## Methods-to-code fidelity
...

## Results-to-source fidelity
...

## Statistical/reporting adequacy
...

## Claim-boundary audit
...

## Figures/tables audit
...

## Blocking scientific changes
1. ...

## Blocking manuscript changes
1. ...

## Optional improvements
- ...

## Maximum permitted claim
> ...

## Submission-prep authorization
AUTHORIZED / NOT_AUTHORIZED

## Evidence inspected
- ...

## Reviewer integrity statement
...
```

A review from another OpenAI GPT/Codex-family model may be useful advisory feedback but cannot satisfy the different-family manuscript review requested here.

## Short prompt to give WorkBuddy

> Independently review ARIS4C Paper 002 at `papers/002-language-geometry/` for manuscript submission readiness. Start with `process/WORKBUDDY_MANUSCRIPT_REVIEW.md` and follow it exactly. Use a fresh non-OpenAI model-family session, independently re-check literature and source evidence, inspect Draft v1 against archived Stage 0–1I reports/code, and write `process/MANUSCRIPT_REVIEW_RECEIPT.md`. Paper 002 is already promoted; your task is manuscript quality, not whether 002 exists.
