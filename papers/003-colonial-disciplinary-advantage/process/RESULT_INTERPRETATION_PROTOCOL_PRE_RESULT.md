# ARIS4C003 — PRE-RESULT INTERPRETATION PROTOCOL

**Frozen:** 2026-09-19  
**Status:** DESIGN_LOCKED / OUTCOME_UNLOCKED; contemporary OpenAlex scan running; no confirmatory effect estimate inspected.

This protocol governs interpretation, not model specification. It prevents the
paper's narrative from being chosen after observing which coefficient is most
favorable.

## 1. No single omnibus verdict

The three confirmatory outcomes address different manifestations of historical
knowledge structure:

1. national disciplinary output composition;
2. field-normalized Top-10% citation impact;
3. international collaboration along former-colonial ties.

They must be reported separately. A result in one outcome cannot substitute
for a null or opposite result in another.

## 2. Report the same evidence bundle for every headline coefficient

For each of the three headline interactions report, regardless of sign:

- log-scale coefficient;
- 95% uncertainty interval;
- multiplicative transform;
- asymptotic clustered p-value;
- complete 999-label-permutation p-value or an explicit INVALID status;
- full 21-field LOO range and sign stability;
- relevant prespecified volume / median-IKES sensitivities.

Do not describe only the statistic that makes the result appear strongest.

## 3. Directional interpretation

A **positive** interaction means that greater historical exposure is associated
with relatively more contemporary activity in disciplines with higher frozen
IKES, conditional on the fixed-effect comparison.

A **negative** interaction means the opposite cross-disciplinary pattern:
greater exposure is associated with relatively more activity in lower-IKES
disciplines, or less activity in higher-IKES disciplines. Negative estimates are
substantive findings and must not be relabeled as model failure.

An estimate near zero / highly uncertain means the frozen analysis did not
detect a stable cross-disciplinary IKES gradient for that outcome. It is not
proof of historical irrelevance in general.

## 4. Outcome-disagreement interpretations

If **output is positive but impact is null/negative**, describe the pattern as
portfolio specialization without corresponding normalized citation advantage;
do not call it general scientific advantage.

If **impact is positive but output is null**, describe a possible influence or
visibility gradient without a broad production-volume gradient.

If **dyadic collaboration is positive while country outcomes are null**, the
data are more consistent with persistence in international knowledge networks
than with national disciplinary specialization.

If **country outcomes are positive while dyadic collaboration is null**, the
pattern is more consistent with domestic institutional/path-dependent
disciplinary structure than with persistence of direct former-colonizer dyads.

If all three outcomes are weak/null, the confirmatory conclusion is that the
frozen broad cross-disciplinary gradient is not supported by these operational
definitions; exploratory field-specific patterns cannot replace that conclusion.

If all three are directionally aligned, describe convergence across outcome
families, while retaining the observational/associational limitation.

## 5. Robustness is diagnostic, not a gate for deleting results

LOO instability, permutation inconsistency, or sensitivity to country-volume
thresholds weakens the claim but does not authorize dropping a discipline or
changing the primary sample.

If a permutation or LOO computation fails, preserve the primary coefficient and
mark that robustness layer invalid. Do not repair it by changing the model after
seeing the result without a dated post-result amendment.

## 6. Temporal profiles

All prespecified periods must be shown.

- Stable coefficients across mature periods are consistent with persistence.
- Declining coefficients are consistent with attenuation over time.
- Increasing coefficients are consistent with strengthening of the measured
  cross-disciplinary association, not necessarily increasing colonial causality.
- Non-monotonic profiles must be described as non-monotonic; no post-hoc
  breakpoint will be promoted to a new primary hypothesis.

The 2023–2025 period is output-only and may not be used as a mature impact test.

## 7. Imperial-center N=8 layer

The imperial-center analysis is corroborative.

Its direction may agree with, disagree with, or be too unstable to inform the
large-sample former-colony result. No N=8 pattern may override the primary
country/dyad models, and no asymptotic p-value treating 8×21 cells as
independent is permitted.

## 8. Causal language

Even strong and robust interactions are described as:

- “associated with”;
- “predicts”;
- “consistent with historical path dependence”;
- “compatible with persistence of historical knowledge structures.”

Avoid:

- “colonialism caused the contemporary discipline advantage”;
- “empire improved science”;
- claims that fixed effects solve historical endogeneity.

## 9. Null-result publication rule

Null, mixed, or sign-reversed headline results do not stop the paper. The
measurement framework, blinded IKES construction, historical exposure audit,
cross-disciplinary test, and falsification structure remain publishable
scientific outputs. The manuscript must report the frozen confirmatory family
rather than converting a null confirmatory study into a positive exploratory
paper.

## 10. Exploratory analyses after the first lock

Any new field-specific, colonizer-specific, ranking, language, mechanism, or
alternative-exposure analysis proposed after the first result package is locked
must be labeled exploratory or post-result sensitivity unless it was already
specified in the preregistration/figure plan.

The first complete result package is SHA-256 locked before human inspection so
the chronology is auditable.
