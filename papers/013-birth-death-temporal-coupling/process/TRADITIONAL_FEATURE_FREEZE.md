# Traditional-calendar feature freeze · ARIS4C013

## Status

**FROZEN v1.0 · FEATURE CONSTRUCTION ONLY.**

This document was frozen before any H3/H4 outcome analysis. It defines the admissible feature families and their exact construction. **Freezing this layer does not authorize mortality-outcome analysis**; that remains controlled by `TRADITIONAL_MODEL_SCHEMA.json`.

## Why this layer is separate

ARIS4C013 distinguishes four levels:

1. ordinary Gregorian timing;
2. official Chinese-calendar encodings;
3. Bazi / fortune-telling conventions;
4. full Four-Pillars calculations requiring birth hour and local-time information.

These are not interchangeable.

## Source conventions already fixed conceptually

### Official Chinese-calendar Gan-Zhi year

For an **official Chinese-calendar** representation, the year changeover follows the first day of the first Chinese-calendar month (Lunar New Year), consistent with the Hong Kong Observatory calendar convention.

This is an H3 cultural-calendar encoding.

### Bazi-style year convention

For the **Bazi-convention** representation, Li Chun / Spring Commences is treated as the alternative year boundary because this convention is widely used in fortune-telling practice.

This is not the same as the official Chinese-calendar year encoding and must remain a separate feature family.

### Solar terms

The 24 solar terms partition the Sun's ecliptic longitude into 24 equal 15-degree sectors.

The astronomical term dates/times are therefore deterministic once the ephemeris and timezone convention are fixed.

## Candidate date-only feature families

### F1 · Official Gan-Zhi year family
Required input:
- exact Gregorian birth date.

Candidate outputs:
- official Gan-Zhi year index 0–59;
- official year stem 0–9;
- official year branch 0–11;
- official zodiac animal branch 0–11.

Boundary:
- first day of the first Chinese-calendar month.

Interpretation:
- cultural-calendar encoding, not Bazi.

### F2 · Bazi-style Gan-Zhi year family
Required input:
- exact Gregorian birth date;
- exact Li Chun boundary date/time.

Candidate outputs:
- Bazi-convention Gan-Zhi year index 0–59;
- stem;
- branch;
- animal branch.

Boundary:
- Li Chun / Spring Commences.

Boundary-date rule:
- if birth time is unavailable and the birth date equals the Li Chun transition date, the year pillar is **ambiguous** and the record is excluded from this feature family rather than guessed.

Interpretation:
- partial Bazi-convention year encoding.

### F3 · Solar-term phase family
Required input:
- exact birth date;
- astronomical solar-term table.

Candidate outputs:
- 24-term bin;
- 12 Jie-bin family;
- days from nearest term boundary.

Boundary rule:
- if exact transition time is required but birth hour is absent, transition-date records are flagged ambiguous.

Interpretation:
- astronomical/calendar representation first; not automatically a metaphysical feature.

### F4 · Bazi-style month-branch family
Required input:
- exact birth date;
- 12 month-opening Jie boundaries.

Candidate output:
- month branch 0–11.

Boundary:
- month-opening Jie solar terms, not Gregorian month and not lunar month.

Records born on a transition date remain ambiguous without time-of-day.

Interpretation:
- partial Bazi-style month encoding; not a full month pillar unless the month stem algorithm is also frozen.

### F5 · Civil-date sexagenary-day family
Required input:
- exact Gregorian date;
- a frozen sexagenary-day reference epoch.

Candidate outputs:
- civil-date 60-day cycle index;
- civil-date stem;
- civil-date branch.

Important label:
- **civil-date sexagenary-day encoding**.

It is not called the person's full Bazi day pillar because birth hour and the disputed day-boundary convention are unavailable.

### F6 · Stem-derived Five-Element family
Only derived from a previously frozen stem.

Fixed basic map:
- Jia / Yi → Wood;
- Bing / Ding → Fire;
- Wu / Ji → Earth;
- Geng / Xin → Metal;
- Ren / Gui → Water.

Polarity:
- alternating Yang / Yin across the ten-stem sequence.

This low-dimensional semantic map is more informative for testing traditional structure than a free 10-level categorical stem model.

## Confirmatory exclusions

The following are **not** allowed into confirmatory H4 until separately sourced, algorithmically frozen, and multiplicity-accounted:

- hour pillar;
- true-solar-time correction;
- full Day Master interpretation;
- Ten Gods;
- hidden stems;
- Na Yin;
- stem combinations;
- branch clashes, harms, punishments, combinations;
- luck pillars / Da Yun;
- favorable/unfavorable element scoring;
- strength/weakness judgments;
- any hand-coded "auspicious" or "inauspicious" rule created after seeing mortality outcomes.

## Full Bazi remains unavailable

A complete Four-Pillars chart requires year, month, day and hour information. ARIS4C013's planned mortality data lack birth hour.

Therefore no H3/H4 result from this project may be described as:
- validation of full Bazi;
- falsification of full Bazi;
- proof of a supernatural mechanism.

The strongest permissible description is a test of **prespecified traditional Chinese date encodings**.

## Critical identifiability point · free categorical labels are not traditional evidence

A free 60-level categorical model for sexagenary year or sexagenary day is invariant to relabeling of the 60 categories.

Likewise, a free 12-level zodiac model is invariant to permutation of the animal names.

Therefore:

> "A 60-level cycle predicts mortality" is not evidence that the traditional semantic labeling is correct.

If every category gets its own unconstrained coefficient, rotating or renaming the cycle simply permutes coefficients and produces the same model fit.

Traditional-structure evidence requires one of:

1. a lower-dimensional traditional semantic mapping fixed in advance;
2. a directional traditional prediction fixed in advance;
3. a relational structure fixed in advance;
4. better held-out performance than matched nontraditional structures that are not mere relabelings.

This prevents a generic periodic cohort effect from being mislabeled as support for Gan-Zhi or Bazi.

## Matched pseudo-systems

### For 5-element / polarity structure
- random 10→5 stem-to-element maps preserving two stems per element;
- random 10→2 polarity maps preserving 5/5 balance;
- combined pseudo semantic maps matched in degrees of freedom.

### For solar-term boundaries
- circularly shifted 24-term boundaries;
- matched 12-boundary pseudo-Jie systems;
- random phase shifts fixed before outcome evaluation.

### For structured stem/branch relations
If any relation family is later admitted, generate random relation graphs with the same node count, edge count and degree distribution.

A simple relabeling of a fully free categorical variable is **not** a valid pseudo-control because it is mathematically equivalent to the original model.

## Model ladder

H3/H4 comparisons occur only after ordinary timing is frozen.

- M0: demographics + cohort + ordinary Gregorian calendar structure;
- M1: M0 + birthday-distance / anniversary terms;
- M2: M1 + official Chinese-calendar encodings;
- M3: M2 + Bazi-style date-only encodings;
- M4: M3 + prespecified traditional semantic structure.

The key question is incremental held-out information, not isolated category p-values.

## Frozen v1.0 artifacts

The feature layer is cryptographically anchored to three Git blobs:

- implementation `traditional_features.py`: `bae8175c91e011bee5fcd5be3d0a1215cc22cb95`;
- reference vectors `TRADITIONAL_REFERENCE_VECTORS.json`: `f080632929b0dc2d916b9915dcbc1f055bd5a7a5`;
- pseudo-system generator `pseudo_calendars.py`: `54d6afcd935f88130c941b36b1e5003ec03422c4`.

Dependency: `lunar_python==1.4.8`.

The feature gate recomputes the Git blob hash of each current file. Editing any frozen file invalidates the gate until a new explicit feature-freeze version is created.

## Outcome model remains locked

Feature construction and outcome analysis are deliberately separated.

`TRADITIONAL_MODEL_SCHEMA.json` is still `frozen=false`. Its gate prevents these frozen features from being connected to H3/H4 mortality outcomes until the source-specific conventional baseline, estimator, scoring rule, analysis code, and multiplicity plan are frozen.

This preserves the pre-outcome status while allowing date encodings themselves to be reproducible and testable.
