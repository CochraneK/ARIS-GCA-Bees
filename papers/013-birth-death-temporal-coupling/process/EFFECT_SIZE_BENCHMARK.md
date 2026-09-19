# Effect-size and equivalence benchmark · ARIS4C013

## Freeze timing

These rules are specified before any population-scale administrative birth-death coupling result is available and before the 1997–2005 holdout is released.

## Primary effect

The primary birthday-coupling effect is the strict offset-0 observed/expected ratio under the exact-birth-year × death-year × sex fixed-margin null.

Interpretation uses relative excess:

- O/E = 1.00: no excess;
- O/E = 1.01: 1% excess;
- O/E = 1.05: 5% excess.

P-values alone are not a decision criterion.

## SESOI / practical-null margin

The smallest effect size of interest is fixed at **±1%**:

- practical-null interval: **0.99 ≤ O/E ≤ 1.01**;
- positive substantive point effect: O/E > 1.01;
- negative substantive point effect: O/E < 0.99.

Rationale: the administrative samples are large enough to make much smaller deviations statistically detectable. A 1% floor is deliberately much smaller than the birthday excesses reported in several prior studies, while preventing a tiny but highly significant deviation from being described as substantively important.

This margin is not changed after discovery.

## Uncertainty

For offset 0, the analysis uses the exact mean and variance of the match count under random pairing with fixed birth/death phase marginals inside each stratum.

Across strata:

- expected counts are summed;
- fixed-margin null variances are summed;
- O/E is observed / expected.

A large-sample delta interval is reported on log(O/E):

- 90% interval for practical equivalence;
- 95% interval for null separation.

This interval is an inferential summary under the fixed-margin model, not a causal confidence interval.

## Practical classifications

### Practically-null-equivalent
The entire 90% interval lies inside [0.99, 1.01].

### Substantive-positive
- point O/E > 1.01; and
- 95% interval excludes 1.00.

### Substantive-negative
- point O/E < 0.99; and
- 95% interval excludes 1.00.

### Statistically-detectable-practically-trivial
- 95% interval excludes 1.00; but
- point O/E remains inside [0.99, 1.01].

### Inconclusive
Anything else.

## Temporal stability

The pooled effect is called temporally stable when at least **7 of 9** annual point estimates in the relevant period are on the same side of 1.00 as the pooled estimate.

This is a prespecified stability diagnostic, not a replacement for the pooled effect.

## Discovery → holdout effect retention

For descriptive comparison:

retention = log(O/E_holdout) / log(O/E_discovery).

Categories:

- ratio < 0: sign reversal;
- 0 to <0.5: attenuated;
- 0.5 to 1.5: magnitude-consistent;
- >1.5: amplified.

The retention category is descriptive. A holdout result is not rejected merely because it is attenuated if it independently satisfies the substantive holdout criterion.

## Confirmatory H2 rule

A **replicated candidate birthday effect** requires all of:

1. discovery and holdout pooled strict effects have the same direction;
2. holdout is classified substantive-positive or substantive-negative;
3. at least 7/9 holdout annual point estimates are in the pooled direction.

If the holdout is practically-null-equivalent, the primary H2 birthday effect is treated as not confirmed even if discovery was significant.

If the holdout is statistically detectable but practically trivial, it is reported as such and is not promoted to a substantive birthday effect.

## Administrative-artifact rule

Raw and strict estimates remain side by side.

A large raw effect that materially shrinks under the locked day-heaping exclusions is interpreted primarily as evidence of administrative date artifacts.

The raw estimate cannot override a strict null result.

## Traditional-calendar separation

These effect-size rules concern ordinary Gregorian birthday/anniversary coupling only.

No H3/H4 cultural or traditional-calendar claim is opened until:

- Pilot 1 discovery is frozen;
- the temporal holdout is evaluated under this benchmark;
- the traditional-calendar feature dictionary is independently frozen.
