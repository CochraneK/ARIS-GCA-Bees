# ARIS4C007 · Pilot 3A universal-clock implementation audit

Last updated: 2026-09-19

## Decision

**PASS — reference implementation reproduced, with a wrapper warning.**

Canonical decision string:

`PASS_REFERENCE_IMPLEMENTATION_WITH_WRAPPER_WARNING`

Pilot 3 may proceed, but the canonical implementation for Universal Mammalian Clock 2/3 is the **Mammalian Methylation Consortium (MMC) v3.0.0 reference code**, not the released MammalMethylClock Clock-3 inverse wrapper.

## Pinned upstream resources

### Mammalian Methylation Consortium

- repository: `shorvath/MammalianMethylationConsortium`
- release: `v3.0.0`
- commit: `44f3329fd593b472c2b6d021d764c9d7e5681f88`
- license: MIT
- reference example bundle: `UniversalPanMammalianClock/ClockParameters/mydata_GitHub.Rds`
- example-bundle SHA-256: `0e70ac93b181928e77cf1372b0fc4aca6ea4163617749c9ad3d4b7d9a3146306`

Reference coefficient hashes:
- Clock 2: `650d3cdf43f10048bd7d84d1ac04bc0b11cf507db6a6c37c9b6f12ebe820c0a3`
- Clock 3: `3c193cf979efa1e277ca469e3b710af19953cc937451f6a6852700a2271a0011`

Reference implementation hash:
- `db85cc18870bea3838a6fad577049d62c91f9ab98e077a06b7a2bbd27e400528`

### MammalMethylClock

- repository: `jazoller96/mammalian-methyl-clocks`
- release: `v1.1.0`
- commit: `a9425df5444863f6431be0ed24845fc35b9f9c83`
- repository license: CC BY-NC-ND 4.0
- release tarball SHA-256: `816bb549307cab5b9fceb736574950322f22371c6e678ecafd52da875c843916`
- Universal coefficient table SHA-256: `70cf2e8117bc23e1d9907eb0a253271af2eb8cc23adfac7e7e7e06a4728ab3b3`

The ARIS4C workflow reads this release in place for audit purposes and does not vendor or redistribute modified package source.

## Bounded official example

The MMC `mydata_GitHub.Rds` example contains:

- **50 samples**
- **1 species:** *Tursiops truncatus* (bottlenose dolphin)

No GSE223748 full methylation matrix was needed for this implementation gate.

## Coefficient parity

### Universal Clock 2

- MMC coefficients: **817**
- MammalMethylClock coefficients: **817**
- missing on either side: **0**
- maximum absolute coefficient difference: **4.62 × 10⁻⁸**

### Universal Clock 3

- MMC coefficients: **761**
- MammalMethylClock coefficients: **761**
- missing on either side: **0**
- maximum absolute coefficient difference: **4.62 × 10⁻⁸**

These differences are at the serialization/rounding level.

## Linear-predictor parity

Applying the two independently distributed coefficient tables to the same official example methylation matrix gives:

- Clock 2 maximum absolute linear-predictor difference: **3.87 × 10⁻⁸**
- Clock 3 maximum absolute linear-predictor difference: **2.93 × 10⁻⁸**

Therefore the coefficient distributions are operationally equivalent at a `1e-6` numerical tolerance.

## Clock 3 inverse-transform audit

The MammalMethylClock documentation describes the Lu et al. Clock-3 relative-adult transform based on:

`m = 5 × (gestation / sexual_maturity)^0.38`

The documented formula reproduces the MMC v3.0.0 reference implementation to numerical precision:

- maximum absolute age difference: **2.84 × 10⁻¹⁴ years**

However, the actual released `v1.1.0` function:

`fun_llinreladult.inv()`

does **not** reproduce the MMC reference transform on the official example.

Across the 50 dolphin samples:

- median absolute difference from MMC Clock 3: **8.78 years**
- maximum absolute difference: **42.14 years**

This is not a coefficient problem: the same coefficients and linear predictors already passed parity.

### Operational rule

For ARIS4C007:

- use the MMC v3.0.0 Clock-3 inverse implementation;
- MammalMethylClock Universal coefficients may be used as a convenient coefficient inventory after hash/version checks;
- do not use the released `fun_llinreladult.inv()` as the canonical Universal Clock-3 inverse unless a later upstream version is independently shown to restore parity.

This is described as an **implementation/documentation drift** in ARIS4C007, not as an attribution of cause or intent.

## Additional reference-script issue

The MMC v3.0.0 example script contains the literal line for Clock 1:

`exp(info[,y.name[k]]) - 2`

after a `for(k in 1:3)` loop, so `k` remains 3. On the bounded example, interpreting that line literally versus using `Y.pred1` changes Clock-1 output by as much as:

**61.25 years**

ARIS4C007 therefore does not use that literal line as independent evidence for Clock 1. Clock 1 must be separately validated against its intended target transformation before inclusion in the equivalence benchmark.

Clock 2 and Clock 3 are unaffected by this indexing issue in the reference script and were independently reproduced above.

## Example chronological-age performance

This is a reproduction diagnostic only, not an equivalence result.

On the 50 bottlenose-dolphin example samples:

- Universal Clock 2 median absolute chronological-age error: **1.91 years**
- Universal Clock 3 median absolute chronological-age error: **2.11 years**

These values do **not** show that either target coordinate is the true biological-age equivalence scale.

## Scientific consequence for 007

Pilot 3A makes the circularity structure explicit:

- Clock 2 is trained against a maximum-lifespan relative-age target;
- Clock 3 is trained against a gestation/maturity relative-adult target;
- their DNAm predictions therefore contain molecular signal **plus the assumptions of their target transformations**.

They cannot be treated as fully independent gold standards for A1/A3.

The molecular axis remains useful if ARIS4C007 distinguishes:

1. the methylation-derived linear predictor;
2. the target transformation used during training;
3. the inverse transformation used to express predictions in chronological years;
4. out-of-species / held-out predictive evidence.

## Next

**Pilot 3B — metadata-first feasibility**

1. acquire GSE223748 metadata without downloading the full beta matrix;
2. inventory species, tissues, age ranges, sex, study/batch and platform;
3. identify overlap with Pilot 0/1/2 species;
4. define a bounded reusable sample before large-data acquisition;
5. preserve training-membership and target-transform circularity flags;
6. only then run molecular/equivalence analyses.

## Handoff sentence

If this chat is lost: **Pilot 3A passed using MMC v3.0.0 as the canonical Universal Clock implementation. MammalMethylClock v1.1.0 Clock 2/3 coefficients reproduce the MMC linear predictors to <1e-6, but its released Clock-3 inverse wrapper differs from the MMC reference by median 8.78 years and max 42.14 years on 50 official dolphin examples. Proceed metadata-first to Pilot 3B; do not use the wrapper as canonical and do not treat Clock 2/3 target coordinates as independent gold standards for A1/A3.**
