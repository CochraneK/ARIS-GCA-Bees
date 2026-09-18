# ARIS4C006 · Frozen leave-one-author-out exposure rule

Last updated: 2026-09-18

## Status

**Frozen before focal surname × outcome estimation.**

The primary field-level alphabetization exposure uses exact **leave-one-author-out (LOAO)** construction.

## Definition

For focal canonical author `i`, target year `t`, and OpenAlex **primary-topic field** `c`:

- convention window = years `t-3 ... t-1`;
- `I_alpha_w = 1` when validated family names on convention work `w` are lexicographically non-decreasing;
- `p_chance_w = prod_j(m_j!) / n_w!` with surname ties.

Total field-window evidence:

`N_ct = sum_w (I_alpha_w - p_chance_w)`

`D_ct = sum_w (1 - p_chance_w)`

Focal-author contribution over lag-window convention works containing canonical author `i`:

`N_ict`, `D_ict`

where each convention work contributes at most once to one author's subtraction.

Primary exposure:

`LOAOExposure_ict = (N_ct - N_ict) / (D_ct - D_ict)`

## Information threshold

Require:

`D_ct - D_ict >= 50`

If this fails, that focal authorship is excluded from the primary mechanism model for that context/year.

The analysis may not choose a different exposure granularity for that record based on the resulting surname-effect estimate.

## Why LOAO

LOAO is preferred to K-fold cross-fitting because:

- lagging already removes the focal work;
- exact subtraction removes the focal author's own prior author-order behavior;
- it avoids fold ambiguity when convention works contain authors from multiple folds;
- it is computationally tractable after convention works and canonical OpenAlex author IDs are materialized.

## QA

The non-LOAO field exposure is retained only for:

- computational validation;
- descriptive comparison;
- assessing how much any individual author contributes to a field-window convention estimate.

It is not the primary confirmatory moderator.

## Related frozen rules

- field assignment: `primary_topic.field.id`, not `topics.field.id`;
- primary context: primary-topic field × prior 3 complete years;
- raw source-level exposure cannot replace field-level exposure;
- 3+ author convention estimates are mandatory robustness;
- raw work-embedded OpenAlex author IDs must be canonicalized before LOAO contribution accounting.
