# Paper 002 · Linguistic Typology submission QA

**QA date:** 2026-09-19  
**Canonical branch:** `main`  
**Build workflow:** `.github/workflows/paper002-build-submission.yml`  
**Final reviewed workflow run:** `35412714647`  
**Build commit:** `608bc871fd4a634a0906b93aeabcd47675e8cb08`  
**Artifact ID:** `10575195098`  
**Artifact digest:** `sha256:d43a6c0e3a136ff71d918a8ce07df05f2a22dead5c38789457b9c3710007d192`  
**Artifact name:** `paper002-linguistic-typology-submission`

## Verdict

**TECHNICAL_SUBMISSION_PACKAGE_PASS**

The scientific manuscript had already received independent `PASS_SUBMISSION_PREP`. This QA verifies the generated submission files rather than re-reviewing the science.

> **Scope warning (added 2026-09-19):** this PASS applies to build commit `608bc871fd4a634a0906b93aeabcd47675e8cb08`, whose journal package contained 3 figures. The canonical EN/ZH manuscripts were later expanded to a 6-figure visual narrative. Therefore this historical PASS must **not** be treated as technical QA of the current six-figure journal package. Rebuild and repeat technical/visual/anonymisation QA before ScholarOne submission.

## Generated files checked

- `Paper002_MANUSCRIPT_BLINDED.docx`
- `Paper002_MANUSCRIPT_BLINDED.pdf`
- `Paper002_TITLE_PAGE_TEMPLATE.docx`
- `Paper002_TITLE_PAGE_TEMPLATE.pdf`
- `Paper002_COVER_LETTER_TEMPLATE.docx`
- `Paper002_COVER_LETTER_TEMPLATE.pdf`
- `Paper002_DECLARATIONS_TEMPLATE.docx`
- `Paper002_ANONYMIZED_SUPPLEMENT.zip`
- 3 separate PNG figures
- figure legends / alt text
- submission metadata checklist
- SHA256 manifest

## Manuscript visual QA

Rendered the final blinded DOCX and final artifact PDF.

- DOCX render: **31 pages**
- artifact PDF render: **31 pages**
- every manuscript page visually inspected
- no clipped text
- no overlapping objects
- no broken/missing glyphs
- no black squares
- figures fit page width and remain legible
- Tables 1–5 fit without clipping
- Table 6 now starts on a fresh page and spans two pages rather than leaving an orphaned first row
- references remain double-spaced; final reference occupies page 31, accepted as a non-blocking layout consequence

A second PDF produced by locally re-rendering the final DOCX also contained 31 pages. Pixel differences against the artifact PDF were small rendering/anti-aliasing differences rather than structural changes.

## Anonymisation QA

Scanned blinded DOCX XML, extracted PDF text, and supplement contents for:

- `CochraneK`
- `Cochrane Kang`
- `WorkBuddy`
- `Tencent`
- `ARIS4C`

**No matches in the blinded manuscript or anonymised supplement.**

DOCX core properties contain no creator name. PDF metadata contains LibreOffice producer information only and no author identity.

## Journal-facing content checks

- abstract: **160 words**
- keywords: **5**, lowercase
- figures 1–3: cited in manuscript and supplied separately
- tables 1–6: present in manuscript
- AI-use disclosure: present
- data-availability statement: present
- funding is kept separate for blinded review
- current manuscript length remains well below the research-paper ceiling documented in the target-journal preparation notes

## Title page / cover letter QA

Title-page template renders cleanly in two pages. Page 2 contains only funding/conflict placeholders.

Cover letter renders cleanly in one page.

No unconfirmed personal metadata were invented. Required author-confirmation placeholders remain explicit.

## Remaining human-only fields

Before submission the author must provide or confirm:

1. IPA transcription of author name;
2. department;
3. institution;
4. street address;
5. city;
6. postal code;
7. country;
8. institutional/corresponding email;
9. ORCID or none;
10. funding statement;
11. conflict-of-interest statement;
12. CRediT roles;
13. originality / not-under-consideration-elsewhere declaration.

Before those fields are used for submission, first rebuild/re-QA the journal package against the canonical six-figure manuscript. After package refresh and the fields above are confirmed, the remaining operation is the actual ScholarOne submission workflow.
