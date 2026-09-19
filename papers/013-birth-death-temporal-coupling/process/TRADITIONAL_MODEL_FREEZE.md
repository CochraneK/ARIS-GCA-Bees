# Traditional-calendar outcome model freeze · ARIS4C013

## Status

**DRAFT / OUTCOME ANALYSIS LOCKED.**

The feature-construction layer is frozen separately. This document governs whether those features may be connected to mortality outcomes.

## Key identification fact

All date-only traditional-calendar features are deterministic transformations of the civil birth date.

Therefore they cannot contain mystical "extra information" beyond the exact birth date in a mathematical sense.

The scientifically meaningful question is instead:

> Does the prespecified traditional representation capture reproducible predictive structure more efficiently or specifically than ordinary calendar representations and matched nontraditional representations of equal complexity?

This changes the interpretation of H3/H4 substantially.

## Consequences

1. A free 60-category Gan-Zhi model cannot support Gan-Zhi semantics; relabeling its categories leaves model fit unchanged.
2. A year-stem or zodiac effect can be confounded with birth cohort unless the source-specific model handles cohort structure.
3. A traditional Five-Element grouping is testable because the 10→5 grouping is a specific compression that can be compared against 1000 balanced random 10→5 groupings.
4. Li-Chun and Jie boundaries are testable as specific boundary placements because shifted boundaries change which observations fall into each interval.
5. A positive traditional-vs-pseudo comparison is evidence of reproducible representation structure, not proof of supernatural causation.

## Draft confirmatory families

### H3 calendar-boundary structure
Official Chinese-calendar and solar-term/Jie representations are tested with omnibus incremental predictive comparisons. Individual category coefficients are descriptive only.

### H4 semantic maps
Four prespecified comparisons:
- Bazi-style year-stem Five-Element map;
- Bazi-style year-stem Yin/Yang map;
- Bazi-style month-stem Five-Element map;
- Bazi-style month-stem Yin/Yang map.

Each traditional map competes against 1000 fixed matched pseudo maps. Empirical pseudo p-value:

[
p = rac{1 + #(	ext{pseudo score} ge 	ext{traditional score})}{1001}.
]

Holm correction is planned across the four semantic comparisons.

### H4 boundary specificity
Two prespecified comparisons:
- Li-Chun year boundary versus fixed pseudo shifts;
- Jie month boundaries versus fixed pseudo shifts.

Holm correction is planned across the two boundary comparisons.

## Why this is not frozen yet

The final analysis model depends on the administrative source actually acquired.

Before model freeze, without inspecting H3/H4 outcome results, the project must lock:
- available covariates and source-quality indicators;
- conventional Gregorian baseline;
- cohort-control functional form;
- outcome target and estimator;
- held-out scoring metric;
- missingness rules;
- source-specific analysis code.

Until those are committed and hashed, H3/H4 outcome analysis remains mechanically blocked even though feature construction itself is reproducible.
