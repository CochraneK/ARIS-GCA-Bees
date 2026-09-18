# ARIS4C007 · Pilot 0 official-data result

Last updated: 2026-09-18

## Status

**Official-data Pilot 0 PASS as a feasibility/measurement-disagreement pilot.**

This is not a biological validation and not a claim that either mapping is a true animal-to-human age conversion.

## Reproducibility

GitHub Actions run: `35300106950`  
Workflow result: **success**

The run completed:
- 5 mapping unit tests;
- direct download of the official AnAge stable ZIP;
- SHA-256 provenance capture;
- extraction of the current `anage_data.txt`;
- deterministic mapping grid construction;
- workflow artifact upload.

Official source manifest from the run:

- AnAge ZIP bytes: **169,150**
- ZIP SHA-256: `e3ddb66e32e973a79932859ba53013e8f60d957c6ec01c6eb573e3ea3018d630`
- extracted `anage_data.txt` SHA-256: `98867969fbd4d0bed6bab415c2715bb19079dbd7f92bdc26e5961856aa1c1519`

Artifact `aris4c007-pilot0`:
- artifact ID: `10529014601`
- artifact SHA-256 digest: `5b15713c2597fad63b39a11ea17b60594f7224cb1d63d7c804ce5e3e02f851fc`

## Coverage

The official AnAge file contained:
- **4,645** species rows;
- **1,349** Mammalia rows;
- **786** mammal rows with gestation + at least one maturity estimate + maximum longevity.

Human is the target/reference species, leaving **785 non-human mammalian species** for this two-coordinate pilot.

At four prespecified source-age positions this produced **3,140 mapping rows**.

## Candidate coordinates compared

### A1 — maximum-lifespan relative age with gestation offset

[
R = \frac{Age + GestationT}{MaxLifespan + GestationT}
]

Source and human ages are matched by equal (R).

### A3 — Lu et al. gestation/maturity log-linear coordinate

The published universal-clock age transformation uses gestation and age at sexual maturity. Pilot 0 maps species by equating this transformed coordinate.

**Important:** applying equal transformed coordinates as an age-equivalence benchmark is our comparison construct. The original clock paper did not establish that this operation is a universal physiological-age truth.

## Descriptive disagreement

Median absolute difference between A1 and A3 human-age outputs:

| Source position | Species | Median absolute difference |
|---|---:|---:|
| sexual maturity | 785 | **3.38 human years** |
| 25% of maximum lifespan | 785 | **10.51 years** |
| 50% of maximum lifespan | 785 | **20.45 years** |
| 75% of maximum lifespan | 785 | **30.47 years** |

At 50% of recorded maximum lifespan:
- mean absolute disagreement: **22.60 years**;
- 90th percentile: **39.14 years**;
- 95th percentile: **46.03 years**.

This demonstrates that the two candidate definitions are not merely separated by one fixed conversion factor.

## Heterogeneity examples

These are illustrations of disagreement, not biological age claims.

At 50% of recorded maximum lifespan, using AnAge entries flagged **high** quality:
- gray wolf: about **0.20 human-year** disagreement;
- cheetah: about **0.76 years**;
- rhesus macaque: about **14.51 years**;
- mouse: about **17.21 years**;
- sheep: about **19.24 years**;
- naked mole-rat: about **82.43 years**.

The existence of both near-agreement and extreme disagreement is useful: it argues against the result being only a trivial global rescaling artifact.

## What Pilot 0 does establish

It establishes feasibility for the core 007 measurement question:

> Defensible cross-species age coordinates can produce materially different mappings on the same species and chronological age, and the size of that disagreement varies across species and life stage.

It does **not** establish:
- which coordinate is biologically superior;
- whether maximum longevity or maturity is measured without bias;
- whether the divergence reflects biology versus construct design;
- whether a latent common age exists.

## Next gate

Pilot 1 must add information that is not algebraically built from the same three life-history traits:

1. held-out life-history/developmental events;
2. independent mortality/survival parameters;
3. published Translating Time event-scale mappings;
4. then molecular/epigenetic clocks.

Only those independent axes can turn disagreement from a descriptive observation into a model-validation problem.
