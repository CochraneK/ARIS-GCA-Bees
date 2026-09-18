# Pilot 1 Discovery Lock · BUNMD / Numident

**Locked before inspecting any ARIS4C013 birth–death coupling outcome in BUNMD.**  
**Date:** 2026-09-18

## Dataset
Berkeley Unified Numident Mortality Database (BUNMD), Harvard Dataverse DOI `10.7910/DVN/TTWNK8`, main archive `bunmd_v2.zip` (Dataverse file id 7128124).

The published codebook reports N = 49,337,827 and contains `byear,bmonth,bday,dyear,dmonth,dday`.

## Data split
- **Discovery:** death years **1988–1996**.
- **Untouched temporal holdout:** death years **1997–2005**.
- Other years are not used for this discovery analysis.

The holdout is not summarized, plotted, tested, or used to change cleaning rules during Pilot 1.

## Eligibility
- valid Gregorian birth and death month/day/year components;
- age at death 18–110 years inclusive;
- exact date components present;
- Feb 29 excluded from the primary 365-day phase representation and counted separately.

## Prespecified administrative-heaping flags
Based on the BUNMD codebook *before coupling outcomes are inspected*:
- birth day-of-month flags: **1, 15**;
- death day-of-month flags: **1, 4, 15**.

The codebook states that surplus counts on these dates suggest SSA may have imputed missing values to them, with patterns differing across periods.

Two discovery estimands are locked:
1. **raw complete-date estimate** — all otherwise eligible complete dates;
2. **strict estimate** — exclude a record if birth day is 1 or 15, or death day is 1, 4, or 15.

The strict estimate is the substantive discovery estimate. The raw estimate is primarily an administrative-artifact diagnostic.

## Birth–death phase
Map month/day to a canonical 365-day non-leap year. For each person:

[
k=(d_{death}-d_{birth}) mod 365.
]

Offset 0 means the same Gregorian month/day.

## Independence null
The expected phase distribution is generated analytically from the observed birth and death day-of-year marginals within:

[
	ext{birth decade} 	imes 	ext{death year} 	imes 	ext{sex category}.
]

Within each stratum, birth and death calendar phases are treated as independently paired while preserving both marginals. Expected offset counts are then summed across strata.

This null therefore preserves:
- seasonality of births;
- seasonality of deaths;
- broad birth-cohort structure;
- death-year-specific calendar structure;
- sex composition;
- known marginal date heaping.

It does **not** solve correlated person-level imputation; that is why the prespecified strict filter exists.

## Discovery outputs
Before any holdout analysis, report:
- raw and strict N;
- offset-0 observed, expected and O/E;
- strict ±30-day O/E profile;
- strict offset-0 O/E separately for each discovery death year;
- birth/death day-of-month histograms;
- rates at all prespecified heaping dates;
- missing/invalid/leap-date counts.

No traditional-calendar/Bazi feature is tested in Pilot 1.

## Interpretation thresholds
Pilot 1 is exploratory discovery, not confirmation.

- A raw spike that materially shrinks under the strict filter is treated as evidence of administrative-date artifacts.
- A strict offset-0 elevation is labeled a candidate birthday/anniversary coupling signal only if it is reasonably stable across discovery years.
- No result from 1988–1996 is called replicated until the frozen specification is applied once to 1997–2005.
- Neither a birthday effect nor any generic birth–death phase dependence is evidence for Bazi.

## Holdout release condition
The 1997–2005 holdout may be opened only after:
1. Pilot 1 code and discovery results are committed;
2. cleaning and null-model rules are frozen;
3. any additional sensitivity analyses motivated by discovery are clearly labeled exploratory and are **not** substituted for the locked primary specification.
