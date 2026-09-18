# ARIS4C007 · Pilot 3 molecular-axis plan

Last updated: 2026-09-18

## Goal

Add a molecular age axis without making the category error:

> high accuracy for predicting chronological age ≠ proof of cross-species biological-age equivalence.

Pilot 3 will use published DNA-methylation clocks as an independent measurement family and ask how their implied age coordinates relate to A1/A3/A4.

## Primary sources

### Lu et al. 2023 universal pan-mammalian clocks

*Nature Aging* 3:1144–1166.

Published dataset:
- 11,754 samples;
- 59 tissue types;
- 185 mammalian species;
- 19 taxonomic orders;
- ages spanning prenatal life to >100 years;
- LOFO and leave-one-species-out validation.

Public data:
- GEO `GSE223748`;
- Mammalian Methylation Consortium data browser.

Public code:
- `shorvath/MammalianMethylationConsortium`;
- tagged release / universal pan-mammalian clock code.

Relevant universal outputs:
- chronological-age clock;
- maximum-lifespan relative-age clock;
- gestation/maturity log-linear clock.

These correspond conceptually to exactly the age-coordinate dispute ARIS4C007 is testing.

### MammalMethylClock

Public repository:
`jazoller96/mammalian-methyl-clocks`

Provides:
- clock coefficients;
- inverse age transformations;
- tutorial/example data;
- many dual human-animal clocks;
- universal mammalian clocks.

This is preferred for a reproducible first application because transformations and coefficients are already harmonized.

## Pilot 3A — code/coefficient reproduction

Before downloading large methylation matrices:

1. pin public clock repositories/versions;
2. reproduce inverse age transformations;
3. apply universal clocks to their public tutorial/example samples;
4. verify predictions against published examples/tests;
5. generate a clock ontology:
   - target construct;
   - training species;
   - tissues;
   - transformation;
   - calibration traits;
   - CpG count;
   - cross-validation design.

Gate:

**No large-data analysis until prediction code reproduces official examples.**

## Pilot 3B — metadata/data feasibility

Use GSE223748 sample metadata to build:
- species;
- chronological age;
- tissue;
- sex;
- array/platform;
- study/batch;
- gestation/maturity/max-lifespan attributes where available.

Do not initially download every methylation beta value if a bounded public subset can validate the workflow.

## Pilot 3C — independent sample benchmark

For reusable public samples:

1. calculate DNAm predictions from universal clocks;
2. preserve published transformation coordinates;
3. compare residuals by:
   - species;
   - life stage;
   - tissue;
   - taxonomic order;
4. use leave-one-species-out results where available rather than only fitted full-model predictions.

## Pilot 3D — equivalence test

Key question:

> When two species are matched by A1, A3 or A4, do independent conserved methylation-age signals become more aligned than under alternative mappings?

Candidate tests:

### D1 — coordinate concordance
Compare rank/continuous concordance between:
- A1 coordinate;
- A3 coordinate;
- universal DNAm clock coordinate.

### D2 — event-conditioned molecular alignment
For species with Pilot 2 event mappings and methylation samples, ask whether molecular residuals are minimized near independently observed homologous event translations.

### D3 — cross-method disagreement
Extend CSAD to include molecular coordinates.

### D4 — species holdout
Use LOSO-compatible outputs or retraining only where computationally feasible; never call full-data fitted predictions independent validation.

## Dual-species clocks

Secondary triangulation:
- human-cat;
- human-rat;
- human-rhesus;
- human-sheep;
- human-pig;
- human-vervet;
- other published dual clocks.

These are useful because they explicitly encode human-animal translation, but each is pair-specific and often uses a life-history transform in its target variable.

Therefore:
- do not treat a dual-species clock as an independent gold standard if its outcome transformation already embeds A1/A3-like assumptions;
- record target-transform dependence explicitly.

## Major confounds

Mandatory:
- tissue;
- batch/study;
- species representation imbalance;
- chronological-age range;
- prenatal/postnatal mixture;
- domestication/breed/strain where relevant;
- platform/probe availability;
- training-set membership;
- target-transform circularity.

## Primary scientific distinction

Separate two questions:

### Prediction
Can DNA methylation predict chronological age across species?

### Equivalence
Does a particular cross-species age transformation align biologically homologous states?

Lu et al. strongly answers the first. ARIS4C007 uses those tools to investigate the second.

## Stop/narrow rule

If methylation raw-data harmonization becomes the dominant project:
- use published LOSO predictions / public tutorial subsets for the primary paper;
- keep full raw methylation reprocessing as a reproducibility extension.

Do not let array preprocessing swallow the central age-equivalence question.

## Next execution

1. pin GitHub repositories/releases;
2. inventory universal clock files and transformations;
3. run official tutorial/example data;
4. freeze a minimal molecular sample benchmark;
5. only then acquire the larger GSE223748 matrix.
