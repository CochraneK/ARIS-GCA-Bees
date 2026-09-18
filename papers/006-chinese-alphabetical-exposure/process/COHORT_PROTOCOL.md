# ARIS4C006 · Cohort and China-based author-year protocol

Last updated: 2026-09-18

## Purpose

Separate the primary work-level author-order mechanism from any downstream person-level career analysis, and prevent the 2024 active-author feasibility seed from becoming a survivor-selected confirmatory cohort.

## 1. Terminology

The study does **not** infer nationality, citizenship, ethnicity, or birthplace from a name.

### China-affiliated authorship

An authorship is `CN-affiliated` when the OpenAlex authorship record contains at least one resolved institution with `country_code = CN`.

### China-based author-year

Candidate rule:

> author `i` is China-based in year `t` when at least one eligible work in year `t` contains a CN-affiliated authorship for that resolved author ID.

Also retain:
- `CN_only`: all resolved institutional countries on eligible authorships in year t are CN;
- `CN_mixed`: CN plus at least one non-CN country;
- `CN_any`: at least one CN affiliation.

The primary author-year rule will be frozen after affiliation-coverage diagnostics. It will never be described as nationality.

## 2. Two separate analysis frames

### Frame A — work/authorship mechanism frame

This is the primary, lower-identity-risk frame.

Unit:
- eligible authorship within an eligible multi-author work.

Requirements:
- validated surname evidence;
- ordered author list;
- independently measured lagged convention exposure;
- China-affiliation status for the focal authorship;
- field/source/year metadata.

This frame does not require reconstructing a complete career.

### Frame B — longitudinal author cohort

This is secondary and remains gated by identity-resolution quality.

Unit:
- resolved author-year.

Frame B is constructed from an **entry rule**, not from scholars observed in a late survivor year.

## 3. Candidate entry-cohort rule

Before outcomes are opened, choose an index period `T0..T1`.

A candidate entrant is a high-confidence resolved author whose:

1. first eligible CN-affiliated scholarly observation occurs in index year `e`;
2. there is a frozen clean-lookback interval immediately before `e` with no eligible scholarly work attributable to that author under the selected OpenAlex corpus;
3. surname evidence passes the frozen Tier 1/2 parser rule;
4. identity-risk score passes the frozen author-resolution threshold;
5. sufficient follow-up exists for the chosen distal endpoint.

Candidate clean lookback: **3 years**. Final value is TBF from coverage diagnostics only.

This rule estimates entry into the *observed eligible scholarly record / China-affiliated frame*, not necessarily a person's true first publication or first academic job.

## 4. Follow-up

Use a common, prospectively frozen follow-up horizon rather than unequal raw career length.

Candidate:
- 5-year follow-up after entry.

Examples:
- entry 2017 -> follow through 2022;
- entry 2020 -> follow through 2025.

No author is called an "exit" merely because no later work appears unless the outcome definition and observation process support that interpretation.

## 5. Right censoring

The last complete publication year must be frozen.

Because 2026 is incomplete at the time of study design, **2026 cannot be treated as a complete outcome year**.

For a 5-year outcome horizon with last complete year 2025, the latest eligible entry cohort would be 2020.

The final complete-year rule will be verified from OpenAlex coverage before freeze.

## 6. Left censoring and established scholars

Authors with substantial pre-index publication history are not forced into an entrant cohort.

They may contribute to:
- Frame A work-level mechanism analyses;
- separate prevalent-author longitudinal sensitivity analyses.

They do not enter the incident/entry cohort merely because a CN affiliation first appears late.

## 7. International and mixed affiliations

Internationalization is both substantively important and potentially endogenous.

Do not simply control it away in every model.

Retain longitudinal states such as:
- CN-only;
- CN + overseas mixed affiliation;
- non-CN-only after prior CN affiliation;
- missing/unresolved.

A mobility analysis, if retained, must distinguish a change in bibliographic affiliation from citizenship or physical migration.

## 8. Career-stage alternatives

If the clean-lookback entry rule proves too sensitive to OpenAlex left coverage, fallback options are:

1. first high-confidence CN-affiliated observation + OpenAlex author `counts_by_year` showing no earlier work in the clean lookback;
2. matched prevalent-author design with explicit observed career age;
3. work-level-only paper, dropping distal career claims.

The fallback is chosen from measurement diagnostics, not from focal surname-effect results.

## 9. Primary longitudinal exposure

For author-year `i,t`:

`PriorAlphaExposure_it`

is constructed only from convention evidence preceding the outcome year and must satisfy the anti-leakage rules in `EXPOSURE_ESTIMATOR.md`.

Surname rank is time invariant; exposure can vary with source, field, collaboration environment, and time.

This supports author fixed effects for the time-varying exposure term and its interaction with a time-invariant surname rank, while the main surname-rank effect itself is absorbed by author fixed effects.

## 10. Survivor-bias rule

The 2024 seed sample used in Pilot 5 is **never** a confirmatory career cohort.

Pilot 5 established only that longitudinal histories are technically retrievable:
- 91.7% of 120 seeds had >=2 active years;
- 65.0% had >=5 active years;
- 75.8% had CN affiliation in >=3 years.

These feasibility proportions cannot be interpreted as population career persistence.

## 11. Minimum identity requirements for Frame B

Before Frame B is unlocked:

- surname measurement gate passed;
- ORCID/OpenAlex consistency pilot completed;
- identity-risk diagnostics reported by surname-rank/frequency strata where feasible;
- frozen exclusion/sensitivity ladder exists;
- no evidence that the apparent rank interaction is carried by high-risk identity records.

If these conditions fail, Frame A remains viable and Frame B is removed from confirmatory claims.

## 12. Frozen language

Allowed:
- China-affiliated authorship;
- China-based author-year under the operational rule;
- affiliation transition;
- observed publication persistence.

Avoid unless independently observed:
- Chinese national;
- Chinese ethnicity;
- emigration/immigration;
- true academic exit;
- first academic job.

## Current status

**Frame A: measurement-feasible.**  
**Frame B: longitudinal data-feasible, identity-gated.**

Exact index years, lookback length, follow-up horizon, and author-year CN rule remain TBF until coverage/identity diagnostics are complete and before focal career outcomes are inspected.
