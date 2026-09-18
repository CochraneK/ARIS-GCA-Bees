# IMPERIAL-CENTER CORROBORATION PROTOCOL — ARIS4C003

**Frozen before confirmatory modern outcomes are inspected.**

This analysis is deliberately **small-N corroboration**. The eight European overseas colonial powers in COLDAT are the independent historical units; repeated disciplines do not create 168 independent imperial histories.

## Units

Imperial centers:

- BEL Belgium
- GBR United Kingdom
- FRA France
- DEU Germany
- NLD Netherlands
- PRT Portugal
- ESP Spain
- ITA Italy

Historical intensity: `cumulative_colony_years_ruled` reconstructed from original COLDAT 3.0 per-power `*_max` start/end intervals.

## Modern period

Primary corroboration window: **2019–2022**.

## Specialization measure

Within the frozen 21-concept mapped OpenAlex universe:

`RCA_cd = (P_cd / P_c) / (P_d / P_all)`

where country attribution follows the primary fractional rule.

Plot/report transform:

`SRCA_cd = (RCA_cd - 1) / (RCA_cd + 1)`.

The reference world is the eligible mapped-country universe, not every geography in OpenAlex.

## Per-empire profile

For each imperial center separately, estimate the descriptive 21-field slope:

`SRCA_d = a + b * IKES_d`.

Also report Spearman correlation between SRCA and IKES.

These per-empire slopes are profile summaries; their naive field-level OLS p-values are not used as evidence of eight independent effects.

## Across-empire corroboration

Relate each empire's profile slope to:

`log1p(cumulative_colony_years_ruled)`.

Report:

- descriptive OLS slope;
- Pearson correlation;
- Spearman correlation;
- all eight raw empire profile slopes;
- leave-one-empire-out slopes.

No asymptotic large-N claim is made with N=8.

## Finite-field falsification

Use **999** IKES-label permutations with seed **20260918**.

For each permutation:

1. shuffle frozen IKES values over D01–D21;
2. recompute all eight empire profile slopes;
3. recompute the across-empire intensity→profile-slope statistic.

The two-sided Monte Carlo p-value is descriptive/falsification evidence, not exact randomization inference.

Any failed/undefined permutation invalidates the permutation layer rather than being silently discarded.

## Interpretation

This analysis can corroborate or contradict the broader historical-knowledge-capital pattern, but it cannot by itself establish a causal effect of empire. The primary large-sample leverage remains the former-colony and former-colonial-dyad analyses.
