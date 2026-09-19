# IMPLEMENTATION CORRECTION 001 — dyad denominator

**Date:** 2026-09-19  
**Design status:** DESIGN_LOCKED  
**Outcome gate:** OUTCOME_UNLOCKED  
**Contemporary OpenAlex outcome materialized before correction:** **NO**

## Frozen rule

The preregistered dyadic rule is:

> for a work with (n) distinct identifiable countries, assign total dyadic
> mass 1 equally across all (n(n-1)/2) unordered country pairs; each pair
> receives (2/[n(n-1)]).

The analysis then retains pairs whose endpoints belong to the frozen current
159-country universe.

## Implementation discrepancy found before first outcome materialization

The first version of `materialize_openalex_dyads.py` joined countries to the
159-country crosswalk **before** counting (n). If a paper contained an
identifiable country outside the analysis universe, the retained countries were
incorrectly renormalized to total pair mass 1.

Example: a paper with countries A, B, X where X is outside the analysis
universe should give A–B mass (1/3). The old implementation would drop X
first and give A–B mass 1.

## Correction

The script now:

1. extracts all distinct identifiable OpenAlex country codes on the work;
2. computes `n_all_identifiable_countries`;
3. joins endpoints to the frozen analysis universe;
4. assigns each retained pair
   `2 / [n_all_identifiable_countries * (n_all_identifiable_countries - 1)]`.

This is an implementation correction to match the already frozen design, not a
new estimand or post-outcome analytic choice.

No modern country×discipline, citation, collaboration, ranking, coefficient,
or p-value was inspected before this correction.
