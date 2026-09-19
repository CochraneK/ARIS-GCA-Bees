# ARIS4C006 · Frozen longitudinal sampling rule

Last updated: 2026-09-19

## Purpose

Freeze how the secondary confirmatory H3 cohort is sampled before any
five-year persistence outcome or surname × exposure coefficient is inspected.

The cohort definition itself remains COHORT_DEFINITION.json. This document
freezes the sampling frame used to obtain candidate entrants.

## 1. Nested sampling frame

H3 is nested inside the already frozen, field-year-balanced primary work frame.

Candidate seed authors are unique canonical OpenAlex authors who appear as
focal rows in the frozen primary work frame during 2014–2020.

No additional random author sample is drawn after this point.

The primary frame itself was selected prospectively as:
- 26 primary-topic fields × focal years;
- deterministic OpenAlex random work blocks;
- field-year-balanced work targets;
- frozen surname and focal-row eligibility.

Therefore H3 inherits a transparent work-seeded sampling scheme rather than
introducing a new post hoc author sampler.

## 2. Entry-year anchoring rule

For each candidate canonical author:

1. record every primary-frame focal-row year in 2014–2020;
2. query the author's complete eligible article/conference-paper history under
   the frozen 2011–2025 corpus rule;
3. determine the first observed eligible publication year e;
4. retain the author only if:
   - e is between 2014 and 2020 inclusive;
   - the author has at least one primary-frame focal row in year e;
   - an eligible work in year e contains a CN-affiliated authorship for that
     author; and
   - the frozen 3-year clean lookback is satisfied.

If an author is sampled only in a later year than their validated entry year,
they are excluded from the confirmatory H3 cohort.

This prevents later survival/persistence from becoming a route into the cohort.

## 3. No secondary subsampling

All validated entrants produced by Section 2 are retained, subject only to the
frozen hard identity exclusions and focal-variable requirements.

Forbidden:
- selecting a subset because persistence rates look favorable;
- selecting only high/low exposure entrants;
- selecting fields or years based on H3 effect size;
- capping common surnames after inspecting persistence;
- replacing the nested cohort with a 2024-active or other survivor sample.

## 4. Sampling interpretation

Because the upstream primary frame samples works, not authors, the resulting
entry cohort is work-seeded rather than author-uniform.

Authors with more eligible entry-year works have a greater chance of appearing
in the upstream work sample.

This is why the frozen H3 model includes EntryWorkCount_i, measured in the
entry year, and why H3 is interpreted as a secondary associational/mechanistic
analysis rather than a population-representative estimate of all Chinese
scholars.

The estimand applies to validated entrants represented by the preregistered
balanced work-seeded frame.

## 5. Field assignment

EntryPrimaryField_i is the OpenAlex primary_topic.field.id of the author's
earliest eligible entry-year work under the reconstructed full history.

If multiple eligible works share the earliest publication date/year and have
different primary fields:
- choose the field of the chronologically earliest dated work where full date
  is available;
- if exact dates tie or are unavailable, choose the numerically smallest
  primary field ID as a deterministic tie-breaker.

No field is selected by outcome strength.

## 6. Early-exposure requirement

After validated entry:
- construct LOAO field exposure for eligible works in e through e+2;
- require at least 2 exposure-defined eligible works;
- MeanEarlyExposure_i is the arithmetic mean across those eligible works.

No weighting by later citation, persistence, venue prestige, or outcome is
allowed.

## 7. Minimum structural adequacy before H3 may run

H3 remains locked unless the outcome-blind cohort build yields:
- at least 1,000 validated entry authors before the >=2 early-exposure-work
  requirement;
- at least 750 authors after all frozen H3 focal-variable requirements;
- all 7 entry years (2014–2020) represented;
- at least 20 of 26 primary-topic entry fields represented;
- at least 100 ORCID-anchored authors;
- at least 500 authors in the frozen low-identity-risk subset.

These thresholds are sample-structure rules only. Persistence values must not
be inspected when deciding whether they pass.

If they fail, H3 is removed from the confirmatory family rather than changing
the sampling rule after outcome inspection. H1/H2 remain unaffected.

## 8. Duplicate seed rows

A canonical author may appear on multiple primary-frame works or in multiple
fields in the same year.

They contribute only once to the H3 candidate set.

All duplicate seed provenance is retained for audit, but duplication does not
increase statistical weight.

## 9. Identity rule

Before cohort inclusion:
- re-resolve embedded OpenAlex IDs to current canonical IDs;
- apply the hard exclusions in IDENTITY_RISK_RULE.md;
- preserve R1–R6 risk flags for mandatory sensitivity analyses.

Names are never used to merge two canonical author entities.

## 10. Outcome lock

The outcome-blind cohort builder may report:
- candidate seeds;
- validated entrants;
- exclusions by reason;
- counts by entry year and primary field;
- ORCID/low-risk subset counts;
- number with >=2 early exposure-defined works.

It may not report:
- Persistence5 prevalence;
- persistence by surname/exposure;
- H3 coefficients or p-values.

Persistence is opened only after the preregistration lock and explicit
confirmatory unlock.
