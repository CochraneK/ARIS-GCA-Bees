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
