# ARIS4C006 · Pilot 4 — randomized surname/identity measurement gate

Last updated: 2026-09-18

## Verdict

**Surname measurement gate: PASS for a high-confidence confirmatory subset.**  
**Person-level identity-resolution gate: supportive but NOT fully passed for distal career outcomes.**

GitHub Actions run: `35297763687`  
Artifact: `aris4c006-measurement-gate`

This is the corrected Pilot 4. An earlier engineering run sampled the first API results and therefore could not estimate coverage. The corrected run used OpenAlex's reproducible random `sample + seed` mechanism within field/year cells, then conditioned on multi-author works.

## Design

- Years: 2015, 2020, 2024
- Fields: Economics, Mathematics, Business, Psychology, Medicine, Engineering
- Target: 40 multi-author works per field/year cell
- Actual sampled multi-author works: **708**
- Surname evidence: DOI -> Crossref structured contributor `family`
- Positional reconciliation: OpenAlex and Crossref list structure plus normalized name-component support
- ORCID used only as an identity/alignment anchor when present
- Aggregate outputs only; no names, DOIs, ORCIDs, or author IDs persisted

## Aggregate results

| Gate metric | Result |
|---|---:|
| Random multi-author works sampled | 708 |
| Works with DOI | 685 / 708 = **96.75%** |
| Crossref records found given DOI | 661 / 685 = **96.50%** |
| Same OpenAlex/Crossref author count | 648 / 661 = **98.03%** |
| Strictly position-supported works among same-count | 629 / 648 = **97.07%** |
| Aligned author pairs | 3,136 |
| Position-supported aligned pairs | **99.11%** |
| Aligned CN-affiliated author pairs | 2,544 |
| CN structured family matched an OpenAlex name token | **99.72%** |
| CN structured family matched the last OpenAlex token | **99.72%** |
| CN position-supported pair rate | **99.37%** |
| Pairs with ORCID in both sources | 342 |
| Exact ORCID agreement when both present | **99.71%** |

Identity lower-bound diagnostics from the sampled aligned records:

- distinct observed ORCID values: **2,339**
- distinct OpenAlex author IDs carrying observed ORCID: **2,339**
- ORCID values observed mapping to >1 OpenAlex ID: **0**
- OpenAlex IDs observed carrying >1 ORCID: **0**

These last two values are **lower-bound diagnostics**, not proof that OpenAlex has no split/merge errors.

## Field/year heterogeneity

Coverage is not perfectly uniform.

The weakest cell in DOI coverage was Economics 2015:

- multi-author works sampled: 28
- DOI coverage: **85.71%**
- Crossref retrieval given DOI: **91.67%**
- strict work-level positional support among same-count records: **90.91%**

Other field/year cells were generally substantially higher.

This means:

1. a Crossref-backed primary sample is technically feasible;
2. missingness/coverage by field and year must be explicitly reported;
3. early-period Economics and any other lower-coverage cells cannot be silently treated as representative complete cases;
4. non-DOI records may enter only through separately validated Tier 1A/2 surname evidence.

## Decision relative to frozen candidate thresholds

The candidate measurement standards in `SURNAME_PARSING_PROTOCOL.md` were:

- >=98% surname-initial precision in included high-confidence Tier 1/2 records;
- >=95% strict positional support for Crossref/OpenAlex same-count work matches;
- no serious ORCID conflict signal;
- field/year coverage documented rather than hidden.

Pilot 4 supports these standards:

- CN structured surname/name compatibility: 99.72%;
- CN positional support: 99.37%;
- strict work-level support: 97.07%;
- ORCID exact agreement: 99.71%.

Therefore Crossref-backed structured-family evidence can be frozen as a confirmatory Tier 1B route.

## What this does NOT establish

Pilot 4 does not establish that:

- DOI/Crossref complete cases are a random sample of all scholarship;
- final-token parsing is acceptable when Crossref/direct evidence is absent;
- OpenAlex person-level author IDs are error-free across entire careers;
- ORCID-linked authors are representative of non-ORCID authors;
- distal career outcomes are ready for confirmatory analysis.

## Identity-resolution interpretation

The absence of ORCID-to-multiple-OpenAlex-ID mappings in this bounded random sample is reassuring but weak evidence about long-horizon person resolution.

The career-outcome analysis remains blocked until a person-level identity-risk audit demonstrates that split/merge risk is not materially structured by surname frequency/rank, or until the analysis is restricted to a sufficiently high-confidence identity subset.

Work-level authorship-order mechanism analyses require much less person-level identity reconstruction and may proceed earlier once exposure construction is frozen.

## Gate consequence

**Surname measurement: PASS.**  
**Work-level research design may proceed.**  
**Distal career-outcome identity gate remains OPEN.**
