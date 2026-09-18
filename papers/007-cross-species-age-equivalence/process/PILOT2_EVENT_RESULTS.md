# ARIS4C007 · Pilot 2 homologous-event benchmark

Last updated: 2026-09-18

## Decision

**PILOT 2 PASS.**

Pilot 2 adds a third, event-rich age-equivalence family and evaluates all methods on the same observed homologous events rather than comparing in-sample fit statistics from unrelated papers.

## Source

Januel et al. (2026), *Biology Open*:

**Cat brains age like humans: translating time shows pet cats live to be natural models for human aging**

- DOI: `10.1242/bio.062604`
- PMCID: `PMC13382973`
- license: CC BY 4.0
- Table S1: **3,754 observations**
- species: cat, human, mouse, chimpanzee
- Table S1 SHA-256: `1bfd115f786fa4c1e911197eadae3451b97b6ace848eaaec61394d76258a1738`
- derived CSV SHA-256: `3f8e30f127d483a433550ca7c56fa3c70366be930cd98d8908a7e176f458905b`
- Dataset 1 R script SHA-256: `383a5b5265df533d411608ba89abc68ab910bcb15824cc5919aa6c5d89cfb8e2`

The official supplements are vendored as text/code under:

`data/sources/translating_time_2026/`

## Data acquisition note

PMC retired its legacy OA Web Service/FTP distribution in August 2026. ARIS4C007 was migrated to the current PMC AWS Cloud Service and successfully acquired the peer-reviewed supplementary files from the article-version prefix.

## Observed-only benchmark

Before reproducing the full imputation/event-scale model, Pilot 2 built a conservative benchmark using only observations directly present in Table S1.

Repeated source records were aggregated with the authors' grouping key:

`Timepoint × Statistics × Sex × Species`

No Amelia imputation was used.

Table S1 produced:

- **1,123** aggregated event keys;
- cat-human observed pairs: **248**;
- mouse-human observed pairs: **261**;
- chimp-human observed pairs: **451**;
- total source→human observed pairs: **960**.

Direct construction-overlap events were then excluded:
- sexual maturity;
- gestation;
- explicit birth-reference events;
- maximum lifespan/longevity if present.

Final strict held-out benchmark:

- **945 event rows**
- **799 source-species × Timepoint clusters**

## Error scale

Primary error:

[
|log_{10}(widehat{PCD}_{human})-log_{10}(PCD_{human})|
]

where PCD is post-conception time.

Median fold error is:

[
10^{median(|log_{10} error|)}
]

This prevents late-life observations measured in decades from mechanically dominating prenatal/developmental observations measured in days.

## Methods

### A1 — maximum-lifespan relative age
Gestation-offset relative age based on maximum lifespan.

### A3 — gestation/maturity log-linear age
Lu et al. universal-clock transformation based on gestation and age at sexual maturity.

### A4 — event-rich pairwise spline, LOTO
A direct adaptation of the pairwise `smooth.spline` models in the Januel et al. authors' Dataset 1:

- cat→human: df = 30;
- mouse→human: df = 12;
- chimpanzee→human: df = 12.

For evaluation, every row sharing a held-out biological `Timepoint` is excluded from model fitting.

This **leave-one-Timepoint-out (LOTO)** design prevents a model from being evaluated on the same event it was trained on.

## Cluster-robust inference

Ordinary event-row bootstrap is insufficient because one biological Timepoint can have multiple sex/statistics variants.

Primary uncertainty therefore resamples:

> **source species × Timepoint clusters**

with 10,000 bootstrap replicates.

For overall and phase analyses, a species-stratified cluster bootstrap is also reported.

## Three-method result

Complete benchmark:

- event rows: **945**
- independent Timepoint clusters: **799**
- A4 extrapolation rows: **6**

### Overall

| Method | Median absolute log10 error | Median fold error |
|---|---:|---:|
| A1 relative lifespan | 0.2435 | **1.75×** |
| A3 log-linear | 0.2282 | **1.69×** |
| A4 event spline LOTO | 0.0872 | **1.22×** |

Cluster bootstrap differences:

### A3 − A1
- observed: **−0.0153**
- 95% CI: **[−0.0475, +0.0071]**

No clear overall A1/A3 winner.

### A4 − A1
- observed: **−0.1564**
- 95% CI: **[−0.1947, −0.1225]**

A4 predicts these held-out homologous events substantially better.

### A4 − A3
- observed: **−0.1410**
- 95% CI: **[−0.1733, −0.1010]**

A4 predicts these held-out homologous events substantially better.

The species-stratified bootstrap gives the same conclusion.

Removing all six A4 extrapolation rows does not materially change the result.

## Species heterogeneity

### Cat → human

Median fold error:

- A1: **2.36×**
- A3: **2.60×**
- A4: **1.16×**

A4 is clearly better than A1/A3.

### Mouse → human

Median fold error:

- A1: **6.13×**
- A3: **7.82×**
- A4: **1.38×**

A4 is dramatically better than the two broad life-history transforms on these events.

### Chimpanzee → human

Median fold error:

- A1: **1.32×**
- A3: **1.20×**
- A4: **1.22×**

Cluster bootstrap:

- A3 is better than A1;
- A4 is better than A1;
- **A4 vs A3 is not clearly separated**:
  - A4 − A3 = +0.0098
  - 95% CI: **[−0.0016, +0.0220]**

Thus a data-rich event model does not automatically dominate the simpler A3 mapping for a closely related primate.

## Life-stage heterogeneity

These are diagnostic human-age bins, not claims that human bins are themselves homologous biological stages.

### Prenatal

Median fold error:
- A1: 5.15×
- A3: 7.17×
- A4: **1.17×**

A4 clearly outperforms both life-history transforms.

### Postnatal 0–2 years

Median fold error:
- A1: 1.37×
- A3: **1.22×**
- A4: 1.35×

Here **A3 clearly outperforms A4**:
- A4 − A3 = +0.0459
- 95% CI: **[+0.0175, +0.0619]**

This is an important method-by-stage reversal.

### Human-age 2–18

Median fold error:
- A1: 1.48×
- A3: 1.37×
- A4: **1.29×**

A4 is better than both, although A3 vs A1 becomes less decisive after cluster correction.

### Human-age 18–60

Median fold error:
- A1: 1.39×
- A3: 1.21×
- A4: 1.17×

A4 beats A1, but **A4 vs A3 is not clearly separated**.

### Human-age 60+

Median fold error:
- A1: 1.42×
- A3: 1.29×
- A4: **1.10×**

A4 is clearly better.

## Main inference

Pilot 2 supports three conclusions.

### 1. Event-rich information matters

A species-pair model trained on hundreds of homologous events can predict other held-out events substantially better than broad life-history scaling.

That is not surprising and must **not** be reframed as evidence that A4 is a universal biological-age truth.

### 2. There is still no universally dominant mapping

Even after giving A4 a large information advantage:
- A3 is competitive with A4 in chimpanzee→human mapping;
- A3 clearly outperforms A4 for the postnatal 0–2 human-age bin.

The best empirical translation depends on species pair and life stage.

### 3. Information requirements are part of the benchmark

A1/A3 need only a few species-level life-history traits and can be applied broadly.

A4 requires a dense homologous-event dataset for each species pair.

Therefore model comparison must include:
- predictive error;
- calibration-data burden;
- taxonomic portability;
- extrapolation behavior;
- uncertainty.

Accuracy alone is not enough.

## Scientific consequence

The central 007 hypothesis is strengthened:

> Cross-species age equivalence is not adequately described by one universally privileged scalar formula. Different coordinates encode different biological information, and predictive performance changes with species, life stage, and the amount of pair-specific calibration data.

The paper should therefore benchmark a **Pareto surface** rather than select one global winner:

[
predictive accuracy 	imes data burden 	imes taxonomic portability 	imes biological construct
]

## Next gate — molecular axis

Pilot 3 adds DNA-methylation age information.

The molecular stage must distinguish:

1. **chronological-age prediction** within/across species;
2. **cross-species age-equivalence validity**.

A clock with high chronological-age correlation does not automatically prove that two organisms with equal clock coordinates are biologically equivalent.

Priority resources:
- Lu et al. 2023 universal pan-mammalian clocks;
- Mammalian Methylation Consortium;
- GEO GSE223748;
- public universal clock code;
- MammalMethylClock coefficients/transformations;
- dual human-animal clocks as secondary triangulation.

## Handoff sentence

If this chat is lost: **Pilot 0, Pilot 1 and Pilot 2 are complete. Pilot 2 benchmarks A1/A3/A4 on 945 strict held-out homologous events (799 Timepoint clusters). A4 is much more accurate overall but does not universally dominate: chimpanzee A3≈A4 and postnatal 0–2 years favors A3. Proceed to Pilot 3 molecular validation; do not collapse chronological DNAm prediction into biological-equivalence claims.**
