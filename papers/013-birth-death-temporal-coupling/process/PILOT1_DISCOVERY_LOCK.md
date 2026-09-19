# Pilot 1 Discovery Lock · BUNMD / Numident

**Revision:** v2 · pre-outcome null hardening  
**Date:** 2026-09-18  
**Outcome-access status at revision:** no BUNMD or raw-NUMIDENT administrative birth–death coupling outcome had been computed or inspected. The first BUNMD run failed at the download gate, and the raw NUMIDENT archives were not present.

## Dataset targets

Primary interchangeable U.S. administrative implementations:

1. Berkeley Unified Numident Mortality Database (BUNMD), Harvard Dataverse DOI `10.7910/DVN/TTWNK8`;
2. raw public-use NUMIDENT Death Files, DOI `10.3886/E207202V1`.

Both contain exact birth and death date components. The same scientific lock applies to both implementations.

## Data split

- **Discovery:** death years **1988–1996**.
- **Untouched temporal holdout:** death years **1997–2005**.
- Other years are not used for this discovery analysis.

The holdout is not summarized, plotted, tested, or used to change cleaning rules during Pilot 1.

## Primary eligibility

Primary phase analyses require:

- complete valid Gregorian birth and death year/month/day components;
- **death year − birth year between 19 and 110 inclusive**;
- Feb 29 excluded from the primary 365-day month/day representation and counted separately.

### Why year-gap eligibility replaces an exact attained-age filter

An exact attained-age filter can mechanically induce birth–death phase dependence at its boundaries.

For example, when `death_year - birth_year = 18`, a person is age 18 only if death occurs on or after the birthday. Therefore selecting `age >= 18` makes inclusion depend directly on the relative birth/death month-day.

A deterministic no-effect toy calculation with all 365 × 365 month-day pairings equally possible but then filtered to the eligible `year_gap=18` pairs gives an offset-0 O/E of approximately **2.98** under a marginal-independence null. This is a pure selection artifact.

Using year gaps **19–110** guarantees that every valid month/day pairing corresponds to an attained age between 18 and 110, so inclusion no longer depends on the birth–death phase.

For transparency, the scripts still count:
- records that would satisfy exact attained age 18–110;
- phase-safe year-gap 19–110 records;
- exact-age boundary records excluded by the phase-safe rule.

The phase-safe set is the locked primary analysis set.

## Prespecified administrative-heaping flags

Based on the BUNMD documentation before coupling outcomes are inspected:

- birth day-of-month flags: **1, 15**;
- death day-of-month flags: **1, 4, 15**.

Two discovery estimands remain locked:

1. **raw complete-date estimate** — all otherwise eligible phase-safe records;
2. **strict estimate** — exclude a record if birth day is 1 or 15, or death day is 1, 4, or 15.

The strict estimate is the substantive discovery estimate. The raw estimate is primarily an administrative-artifact diagnostic.

Raw NUMIDENT exception/source fields are reported diagnostically. They are not allowed to become outcome-informed primary exclusions after coupling results are seen.

## Birth–death phase

Map month/day to a canonical 365-day non-leap calendar. Feb 29 is removed from the primary phase representation.

For each person:

[
k=(d_{death}-d_{birth}) mod 365.
]

Offset 0 means the same Gregorian month/day.

This is a month/day-anniversary representation, not elapsed-day age.

## Primary independence null · v2

The expected phase distribution is generated analytically from the observed birth and death day-of-year marginals within:

[
	extbf{exact birth year} 	imes 	extbf{death year} 	imes 	extbf{sex category}.
]

Within each stratum, birth and death month/day phases are treated as independently paired while both observed marginals are preserved. Expected offset counts are then summed across strata.

This null preserves:

- exact birth cohort rather than only birth decade;
- death-year-specific seasonality;
- sex composition;
- seasonal birth distributions;
- seasonal death distributions;
- marginal administrative date heaping.

### Why exact birth year is primary

A birth-decade stratum mixes cohorts with different mortality ages and potentially different birth-season distributions. In a sample this large, small cohort-composition differences can create measurable phase structure.

Exact birth year is therefore the primary pre-outcome adjustment. Sample size is large enough that this finer stratification is feasible.

## Prespecified coarse-null sensitivity

The original v1 null:

[
	ext{birth decade} 	imes 	ext{death year} 	imes 	ext{sex category}
]

is retained as a **sensitivity analysis**, not erased.

Both raw and strict offset-0 O/E values are reported under:

- the primary exact-birth-year null;
- the birth-decade sensitivity null.

Material disagreement between these nulls is itself evidence that cohort composition matters and must be discussed.

## What the null does not solve

The marginal-independence null does not solve:

- correlated person-level date imputation;
- recording conventions that jointly alter birth and death dates;
- source-specific data-quality mechanisms;
- selective missingness of exact dates.

Those threats are addressed through the strict heaping filter, explicit data-quality diagnostics, source fields where available, and replication.

## Discovery outputs

Before any holdout analysis, report:

- raw and strict N;
- exact-age diagnostic count and phase-safe count;
- boundary records removed by the phase-safe rule;
- offset-0 observed, expected, and O/E under the exact-year null;
- offset-0 O/E under the retained birth-decade sensitivity null;
- strict ±30-day O/E profile;
- strict offset-0 O/E separately for each discovery death year;
- birth/death day-of-month histograms;
- rates at all prespecified heaping dates;
- missing/invalid/leap-date counts;
- raw NUMIDENT exception/source fields where available.

No traditional-calendar/Bazi feature is tested in Pilot 1.

## Interpretation thresholds

Pilot 1 is exploratory discovery, not confirmation.

- A raw spike that materially shrinks under the strict filter is treated as evidence of administrative date artifacts.
- A result sensitive to exact-year versus decade nulls is treated as cohort-composition-sensitive.
- A strict offset-0 elevation is labeled a candidate birthday/anniversary coupling signal only if it is reasonably stable across discovery years and null specifications.
- Statistical significance alone is not sufficient in this very large sample; effect size and replication dominate interpretation.
- No result from 1988–1996 is called replicated until the frozen specification is applied once to 1997–2005.
- Neither a birthday effect nor any generic birth–death phase dependence is evidence for Bazi.

## Holdout release condition

The 1997–2005 holdout may be opened only after:

1. Pilot 1 discovery code and discovery results are committed;
2. this v2 eligibility/null specification is frozen;
3. any additional sensitivity analyses motivated by discovery are clearly labeled exploratory and are not substituted for the locked primary specification.

## Revision history

### v1
- exact attained age 18–110;
- birth-decade × death-year × sex null.

### v2 · current
Changed **before any administrative coupling outcome was available**:
- replaced exact attained-age eligibility with phase-safe year-gap 19–110;
- promoted exact birth year × death year × sex to the primary null;
- retained the v1 birth-decade null as a sensitivity analysis.

Reason: methodological stress testing identified deterministic boundary-selection bias and avoidable cohort aggregation.
