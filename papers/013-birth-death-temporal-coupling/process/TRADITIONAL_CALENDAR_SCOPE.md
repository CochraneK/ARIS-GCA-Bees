# Traditional-calendar scope · ARIS4C013

## Purpose

This document prevents a date-only mortality analysis from being mislabeled as a validation of full Bazi.

The project separates three levels:

1. **ordinary temporal variables** — Gregorian season, day-of-year, cohort, age, weekday and calendar-time effects;
2. **cultural-calendar encodings** — deterministic transformations of a civil date into another calendar representation;
3. **full personal Bazi / Four Pillars** — a birth-chart system requiring information not present in the planned mortality files.

## What date-only mortality data can test

Provided the civil date is valid and sufficiently precise, ARIS4C013 may construct the following prespecified representations.

### A. Chinese sexagenary birth-year encoding
- 60-year stem–branch category;
- 10 heavenly-stem category;
- 12 earthly-branch category;
- 12-animal zodiac category;
- five-element category derived from the heavenly stem;
- yin/yang polarity derived from the stem.

These are deterministic functions of birth year once the year-boundary convention is frozen.

### B. Chinese lunar-calendar date encoding
Potential variables:
- lunar month;
- lunar day;
- leap-month indicator;
- distance to Lunar New Year.

The conversion library/version and calendar convention must be frozen and unit-tested before outcome analysis.

### C. Solar-term / jieqi date encoding
Potential variables:
- 24-solar-term bin;
- days from nearest solar-term boundary.

This is only a calendrical representation unless birth location/timezone and exact time are available.

### D. Sexagenary day encoding
A civil date can be mapped deterministically to a sexagenary-day index under a fixed reference convention.

Because personal birth time and local-day boundary conventions are unavailable, ARIS4C013 must label this a **date encoding**, not a complete personal day pillar.

## What the planned mortality data cannot validly test as “full Bazi”

Full Four Pillars normally requires:
- birth year;
- birth month under the relevant solar-term convention;
- birth day;
- **birth hour**;
- a location/time standard sufficient to resolve local calendar boundaries.

The planned BUNMD / raw NUMIDENT death records do not provide hour of birth. Birthplace may also be absent or too coarse for exact boundary handling.

Therefore:

> No result from ARIS4C013's date-only administrative data may be described as “Bazi validated,” “Bazi disproved,” or a test of the complete Four Pillars system.

The strongest permissible label is **prespecified traditional Chinese date-encoding test**.

## Prediction strategy

ARIS4C013 will not search arbitrary traditional rules until something is significant.

A candidate H4 analysis must compare:

- M0: demographics + cohort + ordinary calendar seasonality;
- M1: M0 + birthday-distance / annual-cycle terms;
- M2: M1 + cultural-calendar encodings;
- M3: M2 + prespecified traditional Chinese date encodings.

The confirmatory question is incremental held-out predictive value, not whether any single category produces p < .05.

## Complexity-matched negative controls

Every traditional feature family receives synthetic comparators with similar flexibility.

Examples:
- permuted labels preserving category frequencies;
- rotated 12-category and 60-category cycles;
- pseudo-lunar calendars with matched month-length structure;
- phase-shifted solar-term bins;
- random partitions with the same degrees of freedom.

A real encoding must outperform the distribution of matched pseudo-systems in untouched data.

## Boundary-convention sensitivity

Chinese calendrical systems have nontrivial boundaries.

Before confirmatory testing the project must freeze:
- whether sexagenary year changes at Lunar New Year or at a solar-term convention such as Lichun;
- the reference timezone for date-only conversions;
- treatment of dates lying on calendar boundaries;
- leap-month handling;
- library/version used for conversion.

Boundary cases should be flagged and analyzed separately rather than silently assigned under whichever library happens to be installed.

## Interpretation ceiling

Even if M3 improves prediction:
- that does not by itself establish a supernatural mechanism;
- cultural/behavioral mediation remains a competing explanation;
- correlated season/cohort structure must be ruled out;
- external replication is required;
- the result applies only to the exact encoded system and conventions that were preregistered.

## Freeze state

**SCHEMA DRAFTED; NOT YET CONFIRMATORY-LOCKED.**

The representation families above can be prepared before Pilot 1, but exact algorithms, boundary conventions, and any directional traditional predictions must be locked before the confirmatory H4 holdout is opened.
