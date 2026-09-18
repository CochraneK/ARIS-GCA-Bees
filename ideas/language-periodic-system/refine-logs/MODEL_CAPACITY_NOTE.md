# Model-Capacity Note · Language Geometry Candidate

## Why this note exists

A hierarchy/tree model can be more structurally flexible than a single circular ordering. Therefore **tree > circular predictive performance is not, by itself, proof that language is intrinsically tree-shaped**. The confirmatory argument must separate two claims:

1. **negative periodic claim:** the tested simple global periodic/circular hypothesis is not supported;
2. **positive geometry claim:** a particular alternative geometry is the true global organization of language.

The current evidence is much stronger for (1) than for (2).

## Capacity sketch

For `n` features:

- **optimized circular model:** `n-1` free angular coordinates after fixing global rotation, plus 3 analytically fitted harmonic coefficients (`1`, `cos(d)`, `cos(2d)`). Reflection remains observationally equivalent. Stage-1B records `n_angular_parameters = n-1`.
- **2-D Euclidean / low-rank representations:** roughly O(2n) latent coordinate/loadings degrees of freedom, subject to rotation/scale/non-identifiability. They are not lower-capacity than the circle in a strict parameter-count sense.
- **hierarchical/tree representation:** data-derived topology plus branch/cophenetic distances; its discrete structural capacity is difficult to reduce to a fair scalar parameter count and can exceed that of a single circle.
- **graph representation:** the most flexible of the screening alternatives and should not be treated as a matched-capacity proof against periodicity.

Because these model classes are not nested and have different discrete/continuous structures, AIC/BIC-style nominal parameter counting would give a misleading sense of exact comparability.

## Why the negative periodic conclusion does not rest only on tree winning

The project added tests that target circularity directly:

- **Stage-1B:** the circle receives direct angular optimization rather than inheriting spectral angles.
- **Stage-1C:** predefined linguistic subsystems are tested without cherry-picking; none satisfy the predeclared combination of predictive competitiveness and circular-order stability.
- **Stage-1D:** a standards-inspired circular-Robinson row-unimodality diagnostic plus an explicit wrap-around closure test is evaluated on held-out families. The circular ordering fails the predeclared support rule at both 40 and 60 features; at 60 features, the mean closure/internal-adjacency ratio is near zero.
- **Stage-1F:** repeated family-held-out comparisons show that tree and low-rank models both outperform the optimized circle on average; the low-rank comparison is useful because its latent parameter scale is not obviously smaller than the circle's.
- **Stage-1H / Stage-1I:** the qualitative tree-over-circle ordering is checked under another independence curation (GBI) and an external sparse source (WALS).

Thus the safe inference is:

> A simple global circular/periodic geometry does not account for the observed cross-linguistic association structure as well as available non-periodic alternatives, and it also lacks direct held-out closure/seriation support.

The unsafe inference would be:

> Human language has been proven to possess a single universal tree geometry.

The latter is **not** supported, especially because geographic/generalization behavior changes by dataset representation.

## Manuscript wording rule

Use phrases such as:

- “predictive evidence favors non-circular structure over a simple periodic geometry”;
- “hierarchical models provide a stronger benchmark under family-held-out evaluation”;
- “the periodic-table hypothesis, in the operationalized global-circle form tested here, is not supported.”

Avoid:

- “language is a tree”;
- “we proved there is no periodicity of any kind”;
- “tree is the true geometry of language.”

## Remaining limitation

A richer periodic family (multiple coupled cycles / toroidal representations) could have greater capacity and might fit better, but introducing it after the simple global circle fails would change the original hypothesis and create substantial researcher degrees of freedom. Such models should be treated as a new, preregistered follow-up question rather than retrofitted to rescue the current hypothesis.
