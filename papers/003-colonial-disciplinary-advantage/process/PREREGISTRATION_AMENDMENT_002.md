# PREREGISTRATION AMENDMENT 002 — confirmatory estimator execution lock

**Date:** 2026-09-18  
**Outcome status at amendment:** real confirmatory country×discipline outcomes remain unopened.  
**Applies to:** `PREREGISTRATION_DRAFT.md` v0.1 + Amendment 001.

This amendment resolves implementation ambiguities before any substantive confirmatory result is inspected.

## A10. Headline period versus persistence analysis

The **headline confirmatory period is 2019–2022**, consistent with the preregistered primary mature window.

Headline models:

1. former-colony fractional output;
2. former-colony Top-10% impact rate;
3. former-colonial-tie dyadic collaboration.

For the 2019–2022 country models, fixed effects are country and discipline.

For the 2019–2022 dyad model, fixed effects are pair, endpoint-i×discipline×period, and endpoint-j×discipline×period.

The non-overlapping periods 2007–2010, 2011–2014, 2015–2018, and 2019–2022 are additionally pooled using the preregistered country×period / discipline×period or dyadic high-dimensional fixed effects. These pooled models are **persistence specifications**, not replacements for the three headline 2019–2022 tests.

## A11. PPML implementation

Primary estimation uses current PyFixest `fepois()`, which implements ppmlhdfe-style Poisson pseudo-maximum-likelihood with high-dimensional fixed effects.

- Output outcome: `fractional_output`.
- Impact outcome: `fractional_top10`, with `offset="log_impact_denominator"`.
- Dyadic outcome: `fractional_collaboration_mass`.
- Separation checks: fixed-effect and iterative-rectifier checks where supported.
- Singleton fixed-effect groups are dropped using the package's standard singleton rule.

The model outcome is permitted to be non-integer because PPML is used as a quasi-likelihood estimator for non-negative fractional mass.

## A12. Main clustered uncertainty

Country models use two-way CRV1 clustering:

`iso3c + concept_id`.

Dyad models use two-way CRV1 clustering:

`pair_fe + concept_id`.

These cluster-robust intervals are reported but are **not treated as sufficient finite-field calibration**, because the discipline dimension contains only 21 clusters.

## A13. Fixed finite-field sensitivity

For each of the three headline coefficients, run a deterministic IKES-label permutation falsification:

- repetitions: **999**;
- RNG seed: **20260918**;
- shuffle the 21 frozen IKES values across the 21 frozen concept IDs;
- preserve countries, dyads, outcomes, exposure values, fixed-effect labels, and sample membership;
- recompute only the exposure×IKES or colonial-tie×IKES interaction;
- re-estimate the identical PPML model;
- two-sided Monte Carlo p-value: `(1 + #(|beta_perm| >= |beta_obs|)) / 1000`.

This is a finite-field falsification/sensitivity analysis, **not exact randomized-treatment inference**.

If any one of the 999 refits fails, the permutation sensitivity is marked invalid and no p-value is silently computed from a reduced successful subset. Any remedy requires a dated amendment.

## A14. Leave-one-discipline-out stability

For each headline model, refit the model 21 times, leaving out D01 through D21 in turn.

Report the complete coefficient distribution. A failed LOO refit invalidates that stability layer rather than being omitted.

The LOO analysis is a robustness/stability diagnostic, not a fourth confirmatory hypothesis.

## A15. Prespecified country-volume sensitivity

For the 2019–2022 country output and Top-10% models, repeat estimation after requiring total mapped fractional output within the country-period across the 21 frozen concepts of at least:

- 50 works;
- 200 works.

These thresholds remain sensitivity analyses and do not redefine the primary sample.

## A16. Median-IKES sensitivity

Repeat the three headline models replacing the equal-weight mean IKES with the adjudicated median across D1–D11.

This is prespecified sensitivity only; the adjudicated equal-weight mean remains primary.

## A17. Failure and provenance policy

`code/run_confirmatory_models.py` writes:

- all six headline/persistence estimates;
- every LOO coefficient;
- every permutation coefficient;
- small-output and median-IKES sensitivities;
- SHA-256 hashes of analysis inputs;
- PyFixest version and deterministic permutation settings.

Model/sensitivity failures are explicit artifacts. They must not be fixed by changing fields, thresholds, samples, or exposure coding after viewing the result without a dated amendment.

## A18. Multiple-testing interpretation

The confirmatory family remains the three headline gradient coefficients.

No single asymptotic p-value, permutation p-value, or ranking result alone defines success. The manuscript must report all three headline estimates irrespective of direction or significance and distinguish primary inference from robustness/falsification layers.
