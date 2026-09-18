# ARIS4C006 · Alphabetization exposure estimator

Last updated: 2026-09-18

## Purpose

Define the institutional moderator independently of focal career outcomes.

The estimator must measure how strongly an author's publication context tends to order collaborators alphabetically **beyond what would occur by chance**, and it must not allow the focal work/author to define their own exposure.

## 1. Eligible convention-measurement works

A work may contribute when it has >=2 listed authors, preserved author order, validated family names for all required authors, publication year/source/field metadata, and a frozen eligible publication type. Crossref structured `family` metadata is preferred for DOI-bearing works after positional reconciliation. Heuristic-only surname parsing is excluded.

## 2. Work-level alphabetization indicator

For ordered normalized family-name keys `s_1 ... s_n`:

`I_alpha = 1` when the sequence is lexicographically non-decreasing, otherwise 0.

Normalization may standardize case, punctuation, diacritics, and documented surname particles, but cannot reorder authors or infer a different surname merely to make a list alphabetical.

## 3. Tie-aware chance probability

For team size `n`, with equal-surname tie groups of sizes `m_1 ... m_k`:

`p_chance = (prod_j m_j!) / n!`

With distinct surnames this is `1/n!`. A two-author distinct-surname work therefore has a 1/2 chance of appearing alphabetical under random ordering, while a four-author work has 1/24.

## 4. Context excess-alphabetization score

For context cell `c`:

`E_c = sum_w (I_alpha_w - p_chance_w) / sum_w (1 - p_chance_w)`

Interpretation:

- `E = 0`: no excess alphabetization above random ordering;
- `E = 1`: every eligible list is alphabetical;
- negative values: less alphabetical than chance.

Negative estimates are not truncated in the primary construction.

## 5. Primary context architecture

Candidate primary context:

**source × OpenAlex field × lagged rolling window**

Candidate lag window: prior 3 publication years.

For a 2024 focal work, for example:

`Exposure(source, field, 2024) <- eligible convention works from 2021–2023`

The final window and fallback hierarchy remain measurement-only TBF until the context-coverage pilot is complete.

## 6. Anti-leakage rule

Primary exposure must satisfy:

1. focal work temporally excluded by lagging;
2. focal author's own prior works removed when computationally feasible.

If exact leave-one-author-out is too expensive at full scale, use K-fold cross-fitting by **author ID**, not by individual work. The estimator is frozen before focal `SurnameRank × Exposure` outcome coefficients are viewed.

## 7. Sparse-cell shrinkage

Define effective information:

`D_c = sum_w (1 - p_chance_w)`

Candidate deterministic shrinkage:

`E*_c = (D_c E_c + lambda D_parent E_parent) / (D_c + lambda D_parent)`

where the parent is a preregistered broader context such as field × rolling window. `lambda`, minimum support, and fallback order are chosen from measurement reliability/coverage only.

## 8. Team-size handling

Primary convention measurement uses all eligible multi-author teams with exact chance correction.

Mandatory robustness:

- 3+ authors only;
- 4+ authors where powered;
- 2-author works separately;
- team-size-stratified exposure.

A result carried only by two-author works is insufficient for the main mechanism claim.

## 9. Time variation

Before retaining a within-author design, quantify:

- within-source temporal reliability;
- between-source variance within fields;
- between-field variance;
- share of scholars with meaningful within-author exposure change.

If exposure is effectively time-invariant for most scholars, the within-author claim is downgraded.

## 10. Permitted measurement-stage inspection

Before outcomes, inspect only:

- context sizes and DOI/Crossref surname coverage;
- `I_alpha`, `p_chance`, and `E_c` distributions;
- adjacent-window reliability;
- source/field/year variance decomposition;
- author-level exposure-switch frequency.

Do **not** inspect focal career-effect interactions while tuning the estimator.

## 11. Candidate fallback hierarchy

To be frozen after the exposure pilot:

1. source × field × lag window;
2. source × lag window;
3. field × lag window;
4. field-level long-run convention.

Fallback is triggered only by predeclared information thresholds.

## 12. Negative controls

- future exposure should not explain prior position;
- shuffled surname rank should eliminate the interaction;
- low-exposure contexts should attenuate the surname-rank gradient;
- single-author outcomes should not show an author-order mechanism;
- non-overlapping author-fold exposure estimates should agree sufficiently with the measurement-only full estimate.

## 13. Gate before confirmatory outcome analysis

Require:

- surname/Crossref measurement gate passed;
- nontrivial between-context exposure variance;
- a substantial repeated-author subset;
- enough within-author exposure change for the proposed fixed-effect analysis;
- frozen lag, shrinkage, sparse-cell, and cross-fitting rules.

If these fail, ARIS4C006 narrows to work-level authorship-order mechanisms rather than forcing a longitudinal career model.
