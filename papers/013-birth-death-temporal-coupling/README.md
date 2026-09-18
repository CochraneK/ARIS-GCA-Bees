# ARIS4C013 · Born to Die?

**Status:** research design / data-feasibility gate open  
**ARIS provenance:** v0.4.26 · `951654847b015585385b2448c5667dcd04e7b56b`

## Working title
**Born to Die? A Falsification-First Test of Birth–Death Temporal Coupling Across Biological, Psychological, Cultural, and Astrological Time Systems**

## Core question
Does the timing of birth contain reproducible information about the timing or cause of death beyond ordinary demographic, seasonal, environmental, and behavioral mechanisms?

The project does **not** treat an observed association as evidence for astrology or Bazi by default. It compares nested explanations.

## Four-layer hypothesis ladder
- **H1 — developmental / seasonal environment:** birth month or season predicts later mortality because it proxies prenatal and early-life exposure.
- **H2 — birthday / anniversary effect:** mortality risk varies with distance from one's birthday.
- **H3 — cultural-calendar effect:** culturally meaningful dates or calendars explain additional timing structure.
- **H4 — traditional calendrical / Bazi incremental prediction:** prespecified Ganzhi, Five-Elements, lunar-calendar, or Bazi-derived features improve out-of-sample prediction after H1–H3 and standard covariates.

H4 is considered supported only by preregistered, independently replicated incremental predictive value.

## Why revisit it?
The relevant literatures already contain (a) month-of-birth/longevity associations, (b) national-scale birthday mortality effects, and (c) a 1993 Chinese-American astrology/mortality claim that failed an independent 2006 replication. This makes the problem ideal for a modern falsification-first design.

## Model ladder
`M0`: conventional demographics + flexible calendar seasonality  
`M1`: M0 + birth-season / early-life temporal features  
`M2`: M1 + birthday-distance / anniversary features  
`M3`: M2 + cultural-calendar features  
`M4`: M3 + prespecified traditional-calendar/Bazi features

## Circular-time analysis
Birth and death dates lie on a circle. Map day-of-year (d) to (	heta=2pi d/L), with (L=365) or 366, and analyze (Delta	heta=(	heta_{death}-	heta_{birth}) mod 2pi).

Planned methods include circular uniformity tests, harmonic/Fourier terms, cyclic GAMs, event-window models, and structure-preserving permutations.

## Strong falsifiers
The strongest interpretation fails if traditional-calendar signals:
- disappear after season/cohort controls;
- fail untouched temporal or geographic replication;
- are matched by pseudo-calendars of equal complexity;
- are unstable across resamples;
- yield negligible predictive gain despite small p-values;
- fit cultural-belief mechanisms better than calendar-intrinsic mechanisms.

## Current gate
**DESIGN INITIALISED / DATA FEASIBILITY OPEN.**

First empirical target: U.S. NVSS mortality microdata from the public-use exact-date era, followed by independent replication where exact dates can lawfully be accessed.
