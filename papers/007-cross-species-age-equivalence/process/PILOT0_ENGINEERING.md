# ARIS4C007 · Pilot 0 engineering smoke test

Last updated: 2026-09-18

## Purpose

This is **not a scientific result**. It tests whether two published life-history coordinate systems can be implemented on the same mammalian table before official raw-data acquisition and full validation.

## Temporary mirror used for smoke testing

Because the current execution environment could identify but not directly fetch the official AnAge ZIP binary, the engineering test read a public GitHub mirror of `anage_data.txt` only to test parsing and transformations.

Mirror file SHA: `6d53329e5788f7bac16e51931b7a9c59ab076e1d`

Observed in that mirror:
- 4,219 total records;
- 1,329 Mammalia rows;
- 672 mammal rows with gestation + at least one sex-specific maturity value + maximum longevity.

This mirror is demonstrably older than the current official AnAge build and therefore **must not be used for manuscript estimates**. Current HAGR documentation reports 4,645 species / 4,671 entries, and the HAGR update table reports 1,349 mammalian entries.

## Transformations implemented

### A1 — maximum-lifespan relative age

[
RelativeAge = \frac{Age + GestationT}{MaxLifespan + GestationT}
]

Species A is mapped to species B by equating this coordinate.

### A3 — Lu et al. log-linear age

[
RelativeAdultAge = \frac{Age + GestationT}{ASM + GestationT}
]

[
\hat m = 5.0\left(\frac{GestationT}{ASM}\right)^{0.38}
]

and the published piecewise log-linear transformation is applied/inverted.

## Smoke-test finding

The implementation is operational and the two candidate coordinates can yield materially different human-equivalent ages for the same source age. The size and direction of disagreement vary strongly by species.

This is exactly the signal 007 is designed to study, but these numbers are not yet interpretable because:
- the mirror is stale;
- maximum-lifespan quality varies;
- equating transformed Clock-3 coordinates is a benchmark construct and not yet independently validated as physiological equivalence;
- no uncertainty is propagated yet.

One useful QC result is that some species show near agreement while others diverge sharply. Therefore disagreement is not a trivial fixed rescaling artifact.

## Engineering safeguards added

- exact formula functions isolated in `code/age_mappings.py`;
- identity and round-trip tests;
- monotonicity tests;
- download/provenance script for official AnAge and Péron et al. supplement;
- output warning that no row is a "true human-equivalent age."

## Next scientific step

Run the same code on the pinned official AnAge release, then:
1. characterize disagreement over all complete mammals;
2. stratify by life stage and data-quality flag;
3. add held-out life-history milestones;
4. add Péron demographic parameters;
5. only then interpret patterns.
