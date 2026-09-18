# ARIS4C006 · Pilot 8 — targeted lagged source-context exposure

Last updated: 2026-09-18

## Verdict

**Source × field × lag-window exposure is feasible, but raw source scores still require reliability-based shrinkage.**

GitHub Actions run: `35298338574`  
Artifact: `aris4c006-source-context-pilot`

Sources were selected **only by lag-window China-affiliated publication volume**, using OpenAlex group-by counts before any author-order score was calculated. This avoids selecting journals because they happened to look alphabetized.

## Design

For target years 2020 and 2024:

- target 2020 exposure window = 2017–2019;
- target 2024 exposure window = 2021–2023;
- fields = Economics, Mathematics, Business, Psychology, Medicine, Engineering;
- select top 2 sources per field by China-affiliated output in the lag window;
- reproducibly sample 40 multi-author works per selected context;
- use Crossref structured family names;
- estimate chance-corrected `ExcessAlpha`;
- repeat with 3+ authors.

## Coverage

- source × field × lag contexts: **24**
- contexts with >=20 valid order works: **24 / 24**
- contexts with >=15 valid 3+ author works: **24 / 24**

Thus the source level is no longer sparsity-blocked in deliberately high-volume contexts.

## Distribution of source-context exposure

Among eligible source contexts:

- 10th percentile: **−0.0436**
- median: **+0.0092**
- 90th percentile: **+0.2731**

For 3+ author works:

- 10th percentile: **−0.0485**
- median: **−0.0051**
- 90th percentile: **+0.2821**

This supports meaningful source-level heterogeneity beyond team-size chance.

## Illustrative high/low contexts

These are measurement examples, not focal surname-effect results.

### Mathematics

- Journal of Mathematical Analysis and Applications:
  - 2017–2019: `ExcessAlpha ≈ +0.351`
  - 2021–2023: `≈ +0.402`
- Journal of Differential Equations, 2021–2023: `≈ +0.708`

### Medicine / Engineering

Several high-volume contexts were close to zero, including major medicine and engineering sources in the sampled lag windows.

The contrast is directionally consistent with the broader field-level pilot.

## Cross-window stability

Only five source × field contexts were selected among the top-volume sources in **both** lag windows.

For those five pairs, the correlation of source-context `ExcessAlpha` across windows was:

**Pearson r ≈ 0.895**

This is encouraging but not sufficient as a reliability estimate because `n=5`.

## Important classification caveat

Some high-output sources are multidisciplinary and appear as top sources in multiple OpenAlex fields (for example Sustainability or Lecture Notes in Computer Science).

Therefore source ID alone is not the convention unit.

The candidate context remains:

**source × field × lag-window**

not merely source.

## Design consequence

Current preferred estimator architecture:

1. raw source × field × lag-window evidence when information is sufficient;
2. shrink source-context scores toward field × lag-window parent estimates;
3. fall back to field × lag-window when source context is unsupported;
4. preserve 3+ author robustness.

The shrinkage strength cannot yet be frozen solely from these 24 contexts.

## Next reliability gate

Use the same independently selected high-volume contexts and split each source convention sample into two deterministic/random halves.

Estimate:

- half-A `ExcessAlpha`;
- half-B `ExcessAlpha`;
- correlation / agreement across source contexts;
- reliability for all multi-author works and 3+ authors separately.

If split-half reliability is weak:
- field × lag-window becomes the primary exposure;
- source-level exposure is exploratory or heavily shrunk.

If split-half reliability is acceptable:
- source × field × lag-window can remain the preferred high-resolution moderator with preregistered shrinkage.

## Current status

**Source-context feasibility: PASS.**  
**Source-context reliability/shrinkage: OPEN.**
