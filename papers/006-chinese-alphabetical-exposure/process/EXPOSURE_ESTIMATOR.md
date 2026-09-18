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

**Frozen primary context after Pilot 10:**

**OpenAlex **primary-topic field** × prior 3 complete publication years**

For a 2024 focal work:

`Exposure(field, 2024) <- eligible convention works from 2021–2023`

Pilot 10 rejected raw source-level exposure as the primary moderator because source-context split-half rank reliability was poor despite acceptable Pearson correlation. This narrowing decision was made before focal surname/career outcomes were inspected.

A source × field × lag-window score may be retained only as a hierarchically shrunk secondary/exploratory exposure.

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

## 11. Frozen exposure hierarchy

Primary confirmatory moderator:

1. **primary-topic field × prior-3-year window**.

Mandatory robustness / secondary:

2. primary-topic field × prior-3-year window using only 3+ author convention works;
3. field-level longer-run convention as a stability sensitivity;
4. source × field × prior-3-year exposure only after hierarchical shrinkage toward the field parent and only as secondary/exploratory.

Raw source-level scores are not eligible to replace the primary exposure because Pilot 10 failed the prospectively frozen Spearman reliability threshold.

## 12. Negative controls

- future exposure should not explain prior position;
- shuffled surname rank should eliminate the interaction;
- low-exposure contexts should attenuate the surname-rank gradient;
- single-author outcomes should not show an author-order mechanism;
- non-overlapping author-fold exposure estimates should agree sufficiently with the measurement-only full estimate.

## 13. Gate before confirmatory outcome analysis

Current status:

- surname/Crossref measurement gate: passed;
- nontrivial between-field/year exposure variance: passed;
- source-level granularity: narrowed to field-level primary after reliability failure;
- repeated-author feasibility: passed;
- within-author exposure-change gate: running;
- final cross-fitting/sample-size rule: must be frozen before outcome unlock.

If within-author exposure variation fails, the paper remains viable as a work-level mechanism study and longitudinal fixed-effect claims are downgraded.


## 14. Prospective source-reliability decision rule

This rule is frozen **before inspecting the split-half reliability artifact**.

The targeted source-context pilot established adequate sample size in high-volume source × field × lag-window cells. The remaining question is whether independently split convention samples rank contexts consistently enough to justify source-level exposure.

Using the deterministic work-ID split defined in `code/10_source_reliability_pilot.py`:

### Source-level primary exposure is allowed when all hold

1. at least 16 source-contexts satisfy the preregistered minimum split support;
2. split-half Pearson correlation of `ExcessAlpha` is >= **0.60**;
3. split-half Spearman rank correlation is >= **0.60**;
4. median absolute difference between half-sample `ExcessAlpha` scores is <= **0.15**;
5. 3+ author split-half estimates have the same broad ordering and do not show a clear collapse inconsistent with the all-team estimate.

If passed, the primary high-resolution moderator becomes:

**shrunk source × primary-topic field × prior-3-year window exposure**

with field × prior-3-year exposure as its parent/fallback.

### Borderline zone

If either Pearson or Spearman lies in **0.40–0.59**, or median absolute difference is **0.15–0.20**, source-level estimates may be retained only as a shrunk secondary/exploratory moderator. The primary confirmatory moderator becomes:

**primary-topic field × prior-3-year window exposure**.

### Source-level rejection

If:
- both reliability correlations are <0.40; or
- median absolute difference exceeds 0.20; or
- 3+ author results qualitatively collapse,

then source-level exposure is not used confirmatorily.

### Rationale

These thresholds are engineering reliability criteria, not significance thresholds and not tuned to any surname/career-effect result. They intentionally favor the coarser field-level exposure if source-level measurement is unstable.


## Primary-field assignment correction

The confirmatory context uses OpenAlex `primary_topic.field.id`, not `topics.field.id`.

Reason: a work may have multiple topics spanning multiple fields, whereas its primary field is uniquely defined by the field of `primary_topic`. Earlier six-field feasibility pilots that filtered on `topics.field.id` are retained only as engineering/anchor evidence and are superseded for confirmatory field assignment by primary-topic-field pilots.

The six anchor fields are not the final scope. All current OpenAlex fields that pass the prospective all-field volume/coverage gate may enter the work-level primary frame.
