# ARIS4C013 Research Plan

## Research question
Test whether birth timing and death timing are statistically dependent and, if so, how much is explained by ordinary seasonality, early-life environment, birthday-related mechanisms, cultural calendars, and prespecified traditional Chinese calendrical/Bazi features.

## Primary estimands
1. **Lifespan by birth phase:** age-specific mortality / survival across birth-time partitions.
2. **Birth–death phase coupling:** deviation of circular birth–death phase difference from an appropriate null.
3. **Birthday event window:** mortality rate at preregistered offsets around the birthday, especially offset 0.
4. **Incremental predictive value:** held-out gain after adding traditional-calendar features to a strong baseline.

Primary metrics: effect sizes with intervals, held-out deviance/log loss, Brier score where appropriate, calibration, and preregistered nested-model comparisons.

## Hypothesis hierarchy
- **H1:** birth season/month predicts lifespan or mortality after basic demographics.
- **H2:** mortality varies around birthdays after seasonality and weekday adjustment.
- **H3:** culturally meaningful calendar representations add information where culturally relevant.
- **H4:** traditional Chinese calendar/Bazi features add replicable information beyond H1–H3.

H1/H2 evidence cannot be redescribed as support for H4.

## Identification threats
Age-period-cohort confounding; seasonal mortality; seasonal fertility and SES selection; migration/latitude; leap years; date heaping/miscoding; coding-practice changes; survivorship conditioning; multiple testing; post-hoc auspicious/inauspicious mappings; psychosocial belief mechanisms; historical-date uncertainty.

## Negative controls
1. Birth-date permutation within year/cohort/location strata.
2. Pseudo-calendars matched on category count/frequency.
3. Rotated calendar labels.
4. Random rule sets matched to Bazi complexity.
5. Prespecified negative-control outcomes.
6. Cross-cultural comparisons where appropriate.

## Validation
Do not rely on random row splits. Prefer discovery years → temporal holdout → geographic holdout → external-country replication. Preserve a final untouched confirmatory set whenever possible.

## Cause-specific analyses
Secondary unless prespecified: cardiovascular/cerebrovascular, suicide, external causes, cancer, infectious disease, and other major groups. Any Five-Elements × organ mapping must be frozen before outcome inspection and must include all null predictions.

## Statistical framework
Cyclic splines/harmonics; Poisson or negative-binomial count models; survival models where valid risk sets exist; circular tests; structure-preserving permutation inference; hierarchical partial pooling; multiplicity control; nested predictive validation.

## Interpretation ladder
- **A:** descriptive temporal non-uniformity.
- **B:** robust association after ordinary controls.
- **C:** mechanism-consistent subgroup/mediator pattern.
- **D:** preregistered traditional-calendar incremental prediction.
- **E:** independent cross-context replication plus failure of matched pseudo-calendar controls.

Only D–E directly address the strongest traditional-calendar claim.
