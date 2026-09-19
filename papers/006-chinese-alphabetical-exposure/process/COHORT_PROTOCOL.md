# ARIS4C006 · Frozen cohort and China-based author-year protocol

Last updated: 2026-09-18

## Purpose

Separate the primary work-level author-order mechanism from the secondary longitudinal extension, while preventing survivor selection and avoiding nationality/ethnicity inference.

Machine-readable contract: `process/COHORT_DEFINITION.json`.

## 1. Terminology

The study does **not** infer nationality, citizenship, ethnicity, birthplace, migration status, or self-identification from a name.

### CN-affiliated authorship

An authorship is `CN-affiliated` when the OpenAlex authorship contains at least one resolved institution with `country_code = CN`.

### China-based author-year

Primary author-year state:

`CN_any = 1` when at least one eligible work in year `t` contains a CN-affiliated authorship for the canonical author.

Retain auxiliary states:
- `CN_only`;
- `CN_mixed`;
- `non_CN_only`;
- `missing_or_unresolved`.

These are bibliographic affiliation states, not nationality.

## 2. Primary work frame

The primary mechanism frame is work/authorship based and is defined in `POPULATION_FRAME.md`.

It does not require a complete career history.

Primary global work window:

**2011–2025**

selected by the prospectively frozen bibliographic coverage gate in `PILOT11_RESULTS.md`.

## 3. Longitudinal entry cohort

Entry years:

**2014–2020**

For a canonical OpenAlex author, entry year `e` is eligible when all hold:

1. the author's **first observed eligible** OpenAlex `article` or `conference-paper` occurs in year `e`;
2. at least one eligible work in `e` contains a CN-affiliated authorship for that author;
3. there is no eligible `article` or `conference-paper` attributed to that canonical author in `e-3 ... e-1`;
4. the surname passes the frozen focal surname-form rule when the author enters a surname-based longitudinal model;
5. the canonical author ID passes the frozen identity engineering rules.

The 3-year lookback is therefore wholly inside the high-coverage era:
- earliest entry 2014 -> lookback 2011–2013.

This identifies **first observed eligible scholarly publication in the corpus**, not first academic job.

## 4. Fixed follow-up

Follow every eligible entrant for **5 years** after `e`.

Latest entry year is 2020 because:
- 2020 + 5 = 2025;
- 2025 is the last complete outcome year in the frozen frame.

The incomplete year 2026 is not an outcome year.

## 5. Frozen distal confirmatory endpoint

### ObservedFiveYearPublicationPersistence

`Persistence5_i = 1` when canonical author `i` has at least one eligible `article` or `conference-paper` in year `e+4` or `e+5`.

Otherwise:
`Persistence5_i = 0`.

Interpretation:
- observed bibliographic persistence in the eligible scholarly record.

It does **not** mean:
- continuous employment;
- annual publishing;
- true academic retention;
- true career exit when 0.

Follow-up work may occur under any affiliation country; persistence is not conditioned on remaining in China.

## 6. Early-career exposure for the distal model

The longitudinal surname/exposure interaction is temporally separated from persistence.

Define early exposure over `e ... e+2`:

1. among eligible article/conference-paper works in `e ... e+2`, retain only works on which the focal author's own authorship is CN-affiliated;
2. assign each retained work its frozen LOAO primary-field prior-3-year exposure;
3. calculate the author's arithmetic mean exposure across those retained early works;
4. require at least **2 exposure-defined CN-affiliated early works** in this window.

Stable surname vulnerability:

`InitialRankNorm_i = (InitialRank_i - 1) / 25`.

Secondary-confirmatory longitudinal interaction:

`InitialRankNorm_i × MeanEarlyLOAOExposure_i`.

The distal model is associational/mechanistic, not a randomized treatment estimate.

## 7. Survivor-bias rule

The 2024 seed used in feasibility pilots is **never** a confirmatory career cohort.

No requirement is imposed that an entrant remains observed in a late calendar year.

Entry is defined prospectively from the first observed eligible work and followed forward for a common horizon.

## 8. Identity rule

Before longitudinal reconstruction:
- resolve every work-embedded OpenAlex author ID to the current canonical author ID;
- preserve original ID for provenance;
- require no known ORCID conflict when ORCID is available;
- do not merge people from raw-name similarity alone.

Pilot 9 repaired all 61/61 raw-ID mismatches through canonical resolution.

Residual non-ORCID split/merge error is addressed through mandatory sensitivity subsets.

## 9. Primary longitudinal model

Secondary confirmatory model:

`logit(Persistence5_i) = alpha + beta1 InitialRankNorm_i + beta2 MeanEarlyExposure_i + beta3(InitialRankNorm_i × MeanEarlyExposure_i) + EntryYearFE + EntryPrimaryFieldFE + f(EntryWorkCount_i)`

Primary longitudinal estimand:
- `beta3`.

`EntryWorkCount` is measured in entry year only.

No citation, prestige, mobility, or later productivity variable is used as a baseline control.

## 10. Missingness and exclusions

For this secondary confirmatory model:
- no surname imputation;
- no exposure imputation;
- no author-ID imputation;
- require the frozen surname form;
- require >=2 early exposure-defined works;
- require complete entry year / primary field;
- missing optional descriptive covariates do not trigger ad hoc imputation.

Authors excluded for missing focal variables are counted and reported by entry year and field.

## 11. Sensitivity ladder

Mandatory:
1. all eligible canonical authors;
2. ORCID-linked authors;
3. uncommon-name / low-collision-risk authors;
4. direct-Han surname subset where available;
5. exclusion of implausible publication/affiliation histories;
6. surname-frequency strata.

The distal result is weakened if present only in high identity-risk records.

## 12. Frozen language

Allowed:
- China-affiliated authorship;
- China-based author-year under the operational rule;
- observed scholarly entry;
- observed five-year publication persistence;
- affiliation transition.

Avoid unless independently observed:
- Chinese national;
- Chinese ethnicity;
- immigration/emigration;
- first academic job;
- true academic exit;
- employment retention.

## Current status

**Frame A work mechanism: research-design ready.**

**Frame B longitudinal extension: retained after feasibility, identity-canonicalization, and within-author exposure-variation gates.**

Its outcome and cohort window are now frozen pre-outcome.
