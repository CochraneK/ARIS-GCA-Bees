# ARIS4C006 · Pilot 5 — longitudinal author-panel feasibility

Last updated: 2026-09-18

## Verdict

**PASS for longitudinal panel feasibility; NOT a confirmatory cohort design.**

GitHub Actions run: `35297727849`  
Artifact: `aris4c006-longitudinal-pilot`

This pilot asks only whether high-confidence China-affiliated authors can be followed across enough OpenAlex years/works/contexts to support a longitudinal exposure architecture.

## Sampling

- Recent seed year: 2024
- Six fields: Economics, Mathematics, Business, Psychology, Medicine, Engineering
- OpenAlex seed works sampled reproducibly with `sample + seed`
- Seed authors required a China-affiliated authorship on a DOI-bearing work whose Crossref structured family name was compatible with the OpenAlex name record
- Maximum authors: 120
- History window: 2015–2024
- Maximum retrieved works per author: 300
- Only aggregate outputs were persisted

## Results

| Feasibility metric | Result |
|---|---:|
| High-confidence seed authors | 120 |
| Seed authors with ORCID | 86 |
| Authors active in >=2 distinct years | 110 (91.7%) |
| Authors active in >=5 distinct years | 78 (65.0%) |
| Authors with >=10 multi-author works | 83 (69.2%) |
| Authors publishing in >=2 sources | 113 (94.2%) |
| Authors publishing in >=3 sources | 103 (85.8%) |
| Authors represented in >=2 OpenAlex fields | 109 (90.8%) |
| Authors with CN affiliation in >=3 years | 91 (75.8%) |
| Median retrieved works | 23.5 |
| Median active years | 8 |
| Median distinct sources | 16.5 |
| Median distinct fields | 5 |
| Active-year IQR | 3–10 years |

## Interpretation

The data structure needed for a longitudinal study exists:

1. most sampled scholars have repeated observations across years;
2. most publish across multiple sources, allowing context exposure to vary;
3. a large majority have multiple China-affiliated years;
4. enough multi-author works exist for author-order mechanisms.

This supports proceeding to an **exposure-switch / context-variance pilot**.

## Critical limitation: survivor/active-author selection

The seed is drawn from scholars observed in 2024. It therefore over-represents scholars who remained active and visible through 2024.

This pilot must **not** define the confirmatory career cohort or estimate persistence/survival effects.

The confirmatory sampling frame should instead be constructed prospectively from an entry/cohort rule, for example:

- first observed eligible publication within a frozen entry window; or
- first stable China-affiliated author-year within a frozen entry window;

followed forward for a common horizon, with left-censoring rules frozen before outcome analysis.

## Field-count caution

The high number of distinct OpenAlex fields per author is useful evidence of contextual variation, but it may partly reflect topic/field classification breadth rather than true disciplinary switching. Field-switching itself is not yet accepted as the primary source of within-author exposure variation.

## Gate consequence

**Longitudinal architecture: GO. Cohort definition: still TBF.**

Next measurement-only requirements:

- quantify actual lagged alphabetization-exposure variance at source/field/year level;
- quantify within-author exposure change;
- freeze sparse-cell/shrinkage and cross-fitting rules;
- construct an entry-based confirmatory cohort rather than using a 2024 survivor seed.
