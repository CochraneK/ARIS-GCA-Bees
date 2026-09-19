# Decisions · ARIS4C013

This file records methodological decisions that should survive chat/session changes.

## D001 · Falsification-first framing
Birth/death timing associations are not treated as evidence of astrology or Bazi by default. Ordinary seasonal, administrative, behavioral, and cultural explanations are modeled first.

## D002 · H1–H4 hierarchy
- H1: developmental / seasonal environment.
- H2: birthday / anniversary timing.
- H3: cultural-calendar representations.
- H4: prespecified traditional Chinese date encodings.

Evidence cannot be promoted upward in this ladder without testing the lower-level alternatives.

## D003 · Exact-date integrity is a hard gate
The NBER/NVSS 1988 mortality layout did not contain exact birth day, so it is not used for paired exact birth–death phase analysis.

## D004 · Wikidata Pilot 0A is artifact-positive, not hypothesis-positive
The very large apparent same-day coupling in Wikidata is dominated by Jan-1/date-precision heaping. It is retained as a methodological demonstration of why exact-looking strings do not guarantee exact dates.

## D005 · Discovery / holdout split
For U.S. Numident administrative data:
- discovery death years: 1988–1996;
- untouched temporal holdout: 1997–2005.

The holdout is not inspected to optimize cleaning, null models, or feature choices.

## D006 · Date-heaping controls are prespecified
Primary raw and strict estimates are both reported. The locked heaping flags are:
- birth day-of-month: 1 and 15;
- death day-of-month: 1, 4, and 15.

Administrative exception/source variables are initially diagnostic. They are not allowed to become outcome-informed primary exclusions after coupling results are seen.

## D007 · BUNMD acquisition is identity-gated
Harvard Dataverse guestbook 506 requires name, email, institution, and position. ARIS4C will not fabricate identity fields. BUNMD remains valid if obtained through a truthful interactive submission.

## D008 · Raw NUMIDENT is the main non-BUNMD fallback
The raw public-use death record contains DOB and DOD components in the same record and includes exception/source indicators. A fixed-width parser is committed and CI-tested.

## D009 · Date-only traditional calendar is not full Bazi
Without hour of birth and sufficient location/time-boundary information, results are labeled traditional Chinese date-encoding tests, not full Four Pillars/Bazi validation or falsification.

## D010 · Matched pseudo-calendars are mandatory for H3/H4
Any cultural/traditional calendar family must compete against synthetic encodings matched for category count or model flexibility. Significance alone is insufficient.

## D011 · Null results remain publishable
The project is successful if it shows that apparent coupling is explained by seasonality, administrative heaping, ordinary birthday effects, or no reproducible signal at all.

## D012 · Phase-safe eligibility replaces exact-age boundary filtering

Before any administrative coupling outcome was available, stress testing showed that exact attained-age eligibility can mechanically induce phase dependence at boundary ages. A toy null with `death_year - birth_year = 18` can produce an offset-0 O/E near 2.98 after selecting age >=18.

Pilot 1 primary eligibility is therefore `death_year - birth_year = 19..110`, which makes inclusion independent of birth/death month-day. Exact age 18–110 is retained only as a diagnostic count.

## D013 · Exact birth-year null is primary

The Pilot 1 primary marginal-independence strata are now:

- exact birth year;
- death year;
- sex category.

The earlier birth-decade × death-year × sex null is retained as a prespecified sensitivity analysis. This change was locked before BUNMD/raw-NUMIDENT coupling outcomes were accessible.

## D014 · Practical-null margin is ±1%

Before administrative discovery results are available, the primary ordinary birthday-coupling SESOI is frozen at O/E 0.99–1.01.

A huge sample may make smaller deviations statistically detectable, but such deviations are not promoted to a substantively meaningful birthday effect.

## D015 · Holdout interpretation is effect-size first

A replicated candidate birthday effect requires:

- same pooled direction in discovery and holdout;
- holdout classified substantive beyond the ±1% margin with its fixed-margin 95% interval excluding 1;
- at least 7 of 9 holdout annual point estimates in the pooled direction.

A 90% interval fully inside 0.99–1.01 is treated as practically-null-equivalent.

## D016 · Temporal holdout requires a two-step repository release

The 1997–2005 holdout cannot be opened by merely editing a boolean.

Release requires:

1. committed discovery result under Pilot 1 v2;
2. a later explicit release-decision commit binding the v2 lock and discovery-result blobs;
3. a still-later release-manifest commit referencing both commits.

The holdout runner validates this chain before opening any data archive.
