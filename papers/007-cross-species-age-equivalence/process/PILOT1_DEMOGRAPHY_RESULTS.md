# ARIS4C007 · Pilot 1 independent demographic benchmark

Last updated: 2026-09-18

## Decision

**PILOT 1 PASS.**

Pilot 1 adds a genuinely independent axis to the life-history mappings: published age-specific mortality-curve parameters from Péron et al. (2019).

The result supports the central ARIS4C007 premise that a single cross-species scalar age definition is not automatically optimal across biologically different events.

## Canonical data chain

### Upstream life-history coordinate source
ARIS4C007 Pilot 0 successful run:

- run ID: `35300650028`
- head SHA: `2a07a9e3e8fade4679d949c221bfb795585071d6`
- complete mammals including human: **786**
- mapping rows: **3,140**
- exact reconstruction error in Pilot 1: **1.31e-11 years**

Pilot 1 consumes the Pilot 0 artifact rather than redownloading AnAge. This freezes all downstream analyses to one canonical life-history snapshot.

### Independent demographic source
Péron et al. (2019), *PLOS Biology*:

> Variation in actuarial senescence does not reflect life span variation across mammals.

- article DOI: `10.1371/journal.pbio.3000432`
- S5 DOI: `10.1371/journal.pbio.3000432.s005`
- published species rows: **96**
- exact overlap with Pilot 0 complete mammals: **88**
- vendored CSV SHA-256: `ec5bd10e21b22769acbb7acd6e930d07ccd64aff9fe048bd179f8c1a6cc4c5fa`
- original XLSX SHA-256: `e7afac6d1b5cc65c1aff523380bc29116bd45d33ad4c303a76c4b338e4a96c30`

The vendored table is the published S5 parameter-estimate table, **not** restricted Species360 individual-level records.

## Mortality-event definitions

Péron et al. define:

- `A`: duration of the juvenile stage;
- `a0`: prime-age minimum/baseline adult mortality;
- `Omega`: age at onset of actuarial senescence;
- `b`: exponential rate of actuarial senescence after onset;
- `A10`: predicted age at which 90% of the cohort is dead (10% survival).

The S5 table stores `Omegatilde`, the duration of the prime-age stage, so:

`Omega = A + Omegatilde`.

These event ages are independent of the AnAge gestation, maturity and maximum-longevity traits used to build A1/A3.

## Compared mappings

### A1 — maximum-lifespan relative age
Uses gestation-offset age divided by gestation-offset maximum lifespan.

### A3 — gestation/maturity log-linear coordinate
Uses the Lu et al. universal-clock age transformation based on gestation and sexual maturity.

No method is declared biological ground truth.

## Evaluation principle

For an event that is intended to represent a homologous demographic transition across species, a useful age coordinate should map that event into a comparatively concentrated target-human age distribution.

Primary descriptive coherence measure:

**MAD = median absolute deviation of mapped human ages.**

Lower MAD is treated as a necessary-style coherence diagnostic only, not proof of biological truth.

A paired species bootstrap (10,000 resamples) estimates:

`MAD(A3) - MAD(A1)`.

Positive values favor A1 on concentration; negative values favor A3.

## Results

### A10 — 10% cohort survival

**88 species**

A1:
- median mapped human age: **91.31 y**
- MAD: **6.55 y**
- IQR: **15.17 y**

A3:
- median mapped human age: **58.76 y**
- MAD: **12.17 y**
- IQR: **26.14 y**

Paired bootstrap:

- `MAD(A3) - MAD(A1) = +5.62 y`
- 95% bootstrap interval: **[+1.06, +9.34]**

**Interpretation:** A1 maps the independent A10 event substantially more consistently across these species than A3.

### End of juvenile mortality stage — A

**88 species**

A1:
- median mapped human age: **7.03 y**
- MAD: **1.32 y**

A3:
- median mapped human age: **4.17 y**
- MAD: **0.99 y**

Paired bootstrap:

- `MAD(A3) - MAD(A1) = -0.33 y`
- 95% bootstrap interval: **[-1.04, -0.01]**

**Interpretation:** A3 has modestly better concentration for this earlier-life demographic transition.

### Onset of actuarial senescence — Omega

**88 species**

A1:
- median mapped human age: **9.30 y**
- MAD: **3.71 y**

A3:
- median mapped human age: **6.54 y**
- MAD: **3.08 y**

Paired bootstrap:

- `MAD(A3) - MAD(A1) = -0.63 y`
- 95% bootstrap interval: **[-3.09, +0.80]**

**Interpretation:** this benchmark does not clearly distinguish A1 and A3 for Omega.

## Main inference

The first independent-axis test rejects the simplest expectation that one of the two age coordinates is uniformly more coherent.

Instead:

- a longevity-position-like event (A10) favors the maximum-lifespan coordinate;
- an early demographic transition (A) slightly favors the gestation/maturity coordinate;
- onset of senescence (Omega) does not clearly choose either.

This pattern is exactly why ARIS4C007 should benchmark **constructs**, rather than search prematurely for one universal conversion formula.

## Important caveats

1. Péron mortality curves derive from zoo/captive cohorts and are not population-invariant biological constants.
2. Some preferred models omit juvenile or prime-age stages, yielding boundary values such as `A=0` or `Omega=A`.
3. A1 can map very early source ages to negative post-birth human ages because its gestation offset allows prenatal human equivalence. These are model outputs, not invalid arithmetic; future reporting will mark prenatal mappings explicitly.
4. Cross-species event concentration is only one criterion. A coordinate could concentrate an event for algebraic or ecological reasons without being a universal biological-time scale.
5. Phylogeny has not yet been incorporated into this 88-species pilot.

## Consequence for 007

The working hypothesis is strengthened:

> Cross-species age equivalence is likely stage- and construct-dependent.

The next independent axis should therefore be a **homologous multi-event event-scale dataset**, not another lifespan-derived proxy.

## Next

Pilot 2:

1. acquire the peer-reviewed Januel et al. (2026) Translating Time Table S1;
2. acquire Dataset 1, the authors' original R age-translation script;
3. reproduce their human/cat/mouse/chimpanzee model;
4. compare A1/A3 predictions against event-scale held-out observations;
5. separate developmental, adult and aging-event subsets;
6. then expand with older Translating Time mammalian/primate datasets.

## Handoff sentence

If this chat is lost: **Pilot 0 and Pilot 1 are complete. Pilot 1 uses 88 mammals and independently published mortality events; A1 is more coherent for A10, A3 is slightly more coherent for juvenile-stage end, and neither clearly wins for senescence onset. Proceed to Pilot 2 by reproducing Januel et al. 2026 Translating Time Table S1 + Dataset 1 before adding methylation clocks.**
