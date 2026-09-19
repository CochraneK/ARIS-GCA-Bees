# Paper 002 · Linguistic Typology submission package

**Primary target:** *Linguistic Typology* (De Gruyter Brill)  
**Package date:** 2026-09-18  
**Scientific status:** independent manuscript-stage review = `PASS_SUBMISSION_PREP`  
**Submission authorization:** AUTHORIZED  
**Current package state:** **SIX-FIGURE REFRESH REQUIRED before ScholarOne**

## Why this target

The manuscript is directly about cross-linguistic structural variation, typological feature organization, limits on diversity, and typological methodology. This is a more direct scope match than reframing the paper around language evolution.

Current journal requirements verified on 2026-09-18:

- submission through ScholarOne;
- all submitted manuscripts must be strictly anonymised;
- a cover letter is required and must briefly state the novelty;
- title page is submitted separately;
- title page requires author names, IPA transcription of author names, affiliations, corresponding-author contact details, short title, word count, figure/table count, and supplementary-material status;
- research papers have a 15,000-word maximum including tables and references;
- tables and figures should be included in the manuscript and also supplied separately;
- AI/ML tools cannot be authors; research/design or methodological use should be disclosed in Acknowledgments.

## Files

- `MANUSCRIPT_BLINDED.md` — strictly anonymised manuscript text.
- `TITLE_PAGE.template.md` — title-page shell; only personal metadata remains.
- `COVER_LETTER.md` — submission cover letter draft.
- `DECLARATIONS.template.md` — funding/conflict/AI/data declarations.
- `SUBMISSION_METADATA_CHECKLIST.md` — minimal fields that still require author input.
- `SUPPLEMENT_MANIFEST.md` — analysis/code files to upload as anonymised supplementary material.

Canonical scientific source remains `../../manuscript/DRAFT.md`. Submission edits must narrow, not broaden, the frozen claim.

## Backup target

*Journal of Language Evolution* is the backup venue. It explicitly welcomes computational/database-driven research articles, including solid negative results, but the current paper is typology-first rather than evolution-first, so *Linguistic Typology* is the cleaner first submission target.


## Current canonical warning · 2026-09-19

The historical 31-page technical QA artifact (workflow run `35412714647`, artifact `10575195098`) passed visual and anonymisation QA, but it was generated when the journal package contained **3 figures**.

The canonical English and Chinese manuscripts now contain **6 figures**. Therefore the historical artifact is provenance only and must not be treated as the final ScholarOne upload.

Before submission:

1. refresh the blinded manuscript and figure bundle from the canonical six-figure manuscript;
2. rebuild with `.github/workflows/paper002-build-submission.yml`;
3. re-run full visual/anonymisation/text-parity QA;
4. update `SUBMISSION_QA.md` and `paper.json` with the new build;
5. then complete author metadata and submit.

Canonical recovery instructions:
`../../process/HANDOFF.md`
