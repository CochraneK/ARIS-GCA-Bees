# SYNTHETIC PPML REPORT — ARIS4C003

Date: 2026-09-18

## Purpose

Stress-test the planned model **before any real colonial-history × contemporary-outcome matrix is opened**.

The synthetic data-generating process uses:

- 80 countries;
- 21 disciplines;
- 4 time windows;
- country×window fixed effects;
- discipline×window fixed effects;
- a continuous country exposure;
- a continuous discipline IKES;
- positive **non-integer fractional outcomes** generated from a Gamma distribution;
- PPML/quasi-Poisson estimation of `exposure × IKES`.

No real country, colonial-history, ranking, citation, publication, or collaboration result is used.

## Deterministic sanity result

Using seed `20260918` and the code path committed in `code/simulate_ppml.py`:

- null DGP (`beta = 0`): estimated interaction ≈ **0.018**;
- signal DGP (`beta = 0.35`): estimated interaction ≈ **0.368**.

This passes the predeclared ±0.12 point-estimate recovery tolerance.

Interpretation: the intended PPML specification can recover a known interaction while accepting fractional, non-integer publication mass. This validates the coding path and supports PPML as a primary count/intensity estimator rather than requiring log-transformed RCA as the only model.

## Important inference warning discovered during stress testing

Repeated synthetic runs showed that **naively treating ordinary cluster-robust p-values as definitive is unsafe for this design**. The coefficient varies across both countries and disciplines, while the confirmatory field set contains only ~21 disciplines. The small number of field clusters makes discipline-side asymptotics fragile.

Therefore:

1. the synthetic gate validates **point-estimate recovery and code path**, not final inferential calibration;
2. final tables should report two-way clustered uncertainty where supported, but should not rely on it alone;
3. confirmatory inference must include a finite-field sensitivity layer, such as an outcome-blindly specified discipline-label/IKES permutation test and leave-one-discipline-out analysis;
4. imperial-center analyses have an additional small-treated-country problem and require leave-one-empire-out / exact-style or permutation-style corroboration rather than pretending repeated discipline rows create many independent imperial histories;
5. the dyadic former-colonial-tie design may provide stronger large-sample leverage because treatment varies across many country pairs, but dependence must still be clustered/blocked appropriately.

## Why this matters

The stress test changed the plan in a useful direction **before** seeing real results. A successful point estimate with an anti-conservative standard error would otherwise create false confidence.

## Gate status

- PPML fractional-outcome code-path gate: **PASS**.
- Final inference calibration gate: **CONDITIONAL / must retain small-cluster and permutation sensitivity analyses**.
- Real outcomes remain unopened for confirmatory testing.
