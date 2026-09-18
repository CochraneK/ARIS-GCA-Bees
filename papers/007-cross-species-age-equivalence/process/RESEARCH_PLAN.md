# ARIS4C007 · Executable research plan

Last updated: 2026-09-18

## 1. Target question

> Do scientifically defensible definitions of cross-species age equivalence converge on a common one-dimensional biological-age scale across mammals, or do developmental, reproductive, demographic and molecular clocks define systematically different notions of "same age"?

Secondary question:

> If they differ, can the disagreement itself be predicted from life-history, ecology, body size, phylogeny, tissue and life stage?

## 2. Why this is not a calculator paper

The public `Animal-Age` repository currently maps birth, sexual maturity, typical lifespan and maximum lifespan to human anchors with piecewise interpolation, while dogs/cats use dedicated tables. That is retained as a transparent heuristic baseline.

For this paper, every mapping is treated as a construct with assumptions, calibration data, uncertainty and a domain of validity. No mapping is declared ground truth by fiat.

## 3. Primary scope

### Confirmatory V1
**Mammalia only.**

Reasons:
- richest shared life-history data;
- pan-mammalian methylation resources exist;
- many dual-species clocks exist;
- enough demographic and developmental subsets exist for validation;
- phylogenetic framework is tractable.

### Later extension
Birds, reptiles, amphibians and fishes are secondary replication/extension domains after V1. Invertebrates are out of confirmatory scope because metamorphosis, caste, semelparity and modular life cycles make "age" less directly homologous.

## 4. Age-equivalence ontology

For species (s) and chronological age (a), define several candidate coordinates.

### A0 — naive lifespan ratio
A linear mapping using typical or expected lifespan.

Purpose: weak baseline analogous to folk "dog years."

### A1 — maximum-lifespan relative age
[
R_{max}(s,a)=a/L_{max,s}
]

Sensitivity variants:
- include gestation offset as in Lu et al.;
- raw AnAge maximum;
- uncertainty-adjusted maximum;
- exclude weak maximum-lifespan records.

### A2 — life-history anchor mapping
Piecewise monotone mapping through homologous life-history events.

Candidate anchors:
- conception/birth;
- weaning where available;
- sexual maturity;
- typical/median lifespan;
- maximum lifespan.

The existing Animal-Age model is the simplest A2 implementation and is a baseline, not the final estimator.

### A3 — log-linear life-history transform
Reproduce the Lu et al. universal-clock age transformation based on gestation and age at sexual maturity, with the published formulation.

Purpose: life-history scaling without requiring direct maximum-lifespan dependence.

### A4 — event-scale / Translating Time mapping
Fit or reproduce event-scale alignment using homologous developmental/physiological/anatomical/behavioral events and smooth monotone curves.

Primary use:
- developmental range across many mammals where available;
- whole-lifespan subsets for primates/cats where published data permit.

### A5 — survival-equivalent age
Define ages as equivalent when they share a demographic position.

Variants:
- equal survival probability (S(a));
- equal cumulative death probability (1-S(a));
- equal remaining life expectancy;
- equal instantaneous mortality hazard after adulthood.

These variants are not assumed identical.

### A6 — molecular/epigenetic age
Use published dual-species and pan-mammalian clocks.

Key distinction:
- chronological-age clocks;
- relative-age clocks;
- log-linear universal clocks;
- age-acceleration residuals.

A clock predicting chronological age well does not automatically validate a biological equivalence mapping.

## 5. Core estimands

### 5.1 Pairwise age mapping
For mapping method (m):

[
f^{(m)}_{Aightarrow B}(a_A)
]

returns the corresponding age in species B.

### 5.2 Cross-method disagreement
For a fixed source species/age and target species:

[
D(A,B,a)=Dispersion_m{f^{(m)}_{Aightarrow B}(a)}
]

Primary dispersion metrics:
- median absolute deviation after target-lifespan normalization;
- interquartile range;
- maximum pairwise difference as descriptive only.

Working label: **Cross-Species Age Disagreement (CSAD).**

### 5.3 Cycle consistency
A candidate common coordinate should approximately satisfy:

[
f_{Cightarrow A}(f_{Bightarrow C}(f_{Aightarrow B}(a))) approx a
]

Define normalized cycle-consistency error over sampled species triples.

This is a structural diagnostic, not proof of biological truth.

### 5.4 Held-out milestone error
Train/define a mapping without selected milestones, then test whether it predicts held-out homologous events.

Candidate held-out events:
- weaning;
- eye opening / locomotor milestones where relevant;
- age at first reproduction;
- skeletal maturation;
- reproductive senescence;
- late-life physiological transitions.

Primary metric:
normalized absolute time error within each species.

### 5.5 Stage-specific disagreement
Estimate disagreement separately across:
- prenatal/developmental;
- juvenile;
- post-maturity prime adulthood;
- senescent/late-life.

The primary hypothesis is non-uniformity across stages, not a predetermined direction.

## 6. Primary hypotheses

### H1 — no universal scalar equivalence
Mechanistically distinct mapping families show non-trivial disagreement beyond measurement uncertainty.

### H2 — stage dependence
Cross-method disagreement varies systematically across the life course.

### H3 — species dependence
Disagreement is associated with life-history traits such as body mass, gestation, maturity timing, longevity and pace-of-life measures after phylogenetic correction.

### H4 — dimensionality
A multi-axis representation explains held-out milestones better than forcing every construct into one scalar age.

### H5 — structural coherence
Methods differ in cycle-consistency error; lower cycle error alone is insufficient for validity but is a useful necessary-condition diagnostic for a common coordinate system.

## 7. Validation hierarchy

No single source is gold standard.

### Tier 1 — independent homologous milestones
Best for testing predictive age alignment.

### Tier 2 — independent molecular data
Test whether life-history mappings align conserved methylation changes not used to build them.

### Tier 3 — demographic curves
Test whether mappings align survival/hazard structure.

### Tier 4 — functional/clinical biomarkers
Use only where standardized comparable outcomes exist (e.g., primate aging biomarkers, dog health/frailty subsets).

Report concordance among tiers rather than collapsing them into one score.

## 8. Data architecture

### Table A — species traits
One row per species:
- taxonomy;
- gestation;
- maturity;
- weaning;
- body mass;
- typical/median lifespan if defensible;
- maximum lifespan + evidence quality;
- data-source provenance.

### Table B — events
One row per species × event:
- event ontology id;
- age/time from conception;
- measurement definition;
- source;
- uncertainty/range;
- data quality.

### Table C — demographic curves
One row per species × age bin:
- survival;
- mortality hazard;
- remaining life expectancy when estimable;
- sex/population/captive-wild metadata.

### Table D — molecular samples
One row per sample:
- species;
- chronological age;
- tissue;
- sex;
- methylation platform;
- clock predictions;
- source study.

### Table E — mapping predictions
One row per source species × source age × target species × method:
- mapped age;
- normalized mapped age;
- extrapolation flag;
- uncertainty;
- method version.

## 9. Open-data source hierarchy

### Life history
1. AnAge/HAGR — curated ageing/longevity reference.
2. Myhrvold et al. amniote database — broad gestation/maturity/weaning/longevity coverage.
3. PanTHERIA — mammalian traits/ecology robustness.

### Molecular
1. Mammalian Methylation Consortium resources.
2. `MammalMethylClock` coefficients/transformations.
3. Public supplementary/sample metadata from dual-species clock papers.

### Development/event alignment
1. Translating Time / Workman et al. 2013 event model.
2. Charvet et al. 2023 primate lifespan alignment supplementary data.
3. 2026 cat-human whole-lifespan alignment supplementary data when reusable.

### Demography
1. published supplementary mortality-curve parameters for 96 mammals (Péron et al. 2019);
2. open life-table/lifespan studies;
3. COMADRE matrix population models;
4. Primate Aging Database / Primate Life History resources where access permits.

Species360 raw data are optional; V1 must not depend on privileged access.

## 10. First pilot species set

Select species to maximize overlap, phylogenetic spread and scientific importance rather than convenience.

Candidate seed:
- human;
- rhesus macaque;
- chimpanzee;
- domestic dog;
- domestic cat;
- mouse;
- rat;
- rabbit;
- sheep;
- naked mole-rat;
- one bat;
- one cetacean;
- one ungulate;
- one marsupial.

Final seed is determined by frozen data-completeness criteria.

## 11. Model comparison protocol

### Step 1 — deterministic reproduction
Implement A0–A3 without fitting outcome-aware parameters.

### Step 2 — event model reproduction
Reproduce a published Translating Time subset.

### Step 3 — demographic mapping
Construct A5 for species with adequate mortality information.

### Step 4 — molecular mapping
Apply published A6 clocks to available datasets.

### Step 5 — common evaluation grid
For each eligible species, evaluate a prespecified set of normalized age quantiles and observed event ages.

### Step 6 — disagreement analysis
Estimate CSAD overall and by life stage.

### Step 7 — trait/phylogeny analysis
Model disagreement and method residuals using phylogenetic comparative models.

### Step 8 — latent model only after benchmark
Only if multiple axes show enough common structure, estimate a latent/multi-view biological-time model.

## 12. Phylogenetic design

Mandatory:
- species phylogeny with branch lengths from a documented mammalian tree;
- phylogenetic signal of residuals;
- PGLS or phylogenetic mixed/hierarchical models for trait associations;
- leave-one-species-out validation;
- leave-one-order-out validation for generalization;
- report effective taxonomic breadth rather than raw species N alone.

No standard random split can be the only validation.

## 13. Uncertainty

Propagate uncertainty from:
- maximum-lifespan record quality;
- gestation/maturity ranges;
- event timing ranges;
- spline/model prediction intervals;
- mortality curve parameter error;
- epigenetic clock prediction error.

Use bootstrap/Bayesian propagation where appropriate.

The output should be an interval or distribution, not only a single "human-equivalent age."

## 14. Robustness / falsification

Minimum set:
- maximum lifespan vs alternative longevity denominator;
- raw vs quality-filtered longevity records;
- male/female demographic curves where available;
- captive vs wild populations where separable;
- exclude domestic species;
- exclude primates;
- leave-one-order-out;
- life-history only vs molecular only;
- developmental-only vs post-maturity-only;
- methods trained on source-target pair excluded from independent benchmark where applicable;
- random/event-label permutation falsification for event-alignment models.

## 15. Primary figures

1. **Method atlas:** conceptual diagram of age axes.
2. **Human-equivalent fan plots:** several species showing all mappings across age.
3. **Disagreement heatmap:** species × life stage.
4. **Cycle-consistency network:** mapping loops and error.
5. **Held-out milestone benchmark:** model error distribution.
6. **Phylogenetic map:** where disagreement is high/low on the mammal tree.
7. **Multi-dimensional age space:** only if supported.

## 16. Relationship to Animal-Age

`CochraneK/Animal-Age` becomes:
- a source of one transparent baseline;
- a public demonstrator;
- later, an interactive supplement for uncertainty-aware multi-axis outputs.

Scientific code/data live in ARIS4C007. The public calculator must not silently turn exploratory mappings into authoritative veterinary or biological advice.

## 17. Stop / narrow rules

Narrow the paper if:
- only two mapping families can be reproduced on a meaningful shared species set;
- source definitions are too heterogeneous to construct comparable held-out events;
- molecular raw/sample data cannot be reused and only published aggregate outputs exist;
- phylogenetic coverage collapses to one narrow clade.

If broad pan-mammal integration fails, a strong fallback is a deeply validated mammal subset (e.g., primates + dog + cat + rodents) rather than forcing breadth.

## 18. Current decision

**ARIS conditional GO to data-acquisition and benchmark-pilot stage.**

The central claim is not that a new formula is already correct. The study tests whether the premise of a unique cross-species equivalent age is itself empirically supportable.
