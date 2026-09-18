# STATUS — ARIS4C007

**Last updated:** 2026-09-18  
**State:** `PILOT1_DEMOGRAPHY_COMPLETE / PILOT2_TRANSLATING_TIME_ACQUISITION`  
**ARIS provenance:** v0.4.26 @ `951654847b015585385b2448c5667dcd04e7b56b`

## Canonical research identity

**Are Animal Years Comparable? Benchmarking Cross-Species Biological Age Equivalence Across Mammals**

The project is no longer framed as merely inventing a better "animal years" calculator. The scientific target is whether different defensible definitions of equivalent biological age yield a coherent common scale across species.

## Completed

- [x] Existing `CochraneK/Animal-Age` prototype inspected.
- [x] Current 103-species anchor model identified as a useful heuristic baseline, not a gold standard.
- [x] Found direct adjacent traditions: physiological/developmental equivalence, Translating Time, mortality/senescence comparison, dual-species clocks, universal pan-mammalian clocks.
- [x] Found 2026 human-cat whole-lifespan Translating Time paper; novelty claim narrowed accordingly.
- [x] Primary taxonomic scope frozen to Mammalia for V1.
- [x] Model-family benchmark defined.
- [x] Primary evaluation concepts defined: held-out milestone error, method disagreement, uncertainty, and cycle consistency.
- [x] Open/public data hierarchy drafted.
- [x] Phylogenetic non-independence declared mandatory rather than optional.
- [x] Animal-Age retained as prototype/interactive downstream asset rather than treated as evidence.
- [x] Pilot 0 deterministic mapping engine implemented (relative-lifespan and Lu log-linear coordinates).
- [x] Round-trip, identity and monotonicity QC tests added.
- [x] Reproducible public-source downloader with SHA-256 provenance added.
- [x] Engineering smoke test run on a stale public AnAge mirror: 1,329 mammal rows, 672 with gestation + maturity + maximum-longevity completeness.
- [x] Smoke test confirmed species- and stage-dependent disagreement is technically measurable; no smoke-test number is treated as a scientific estimate.
- [x] Official AnAge Pilot 0 completed successfully on GitHub Actions run `35300106950`.
- [x] Official build: 4,645 species rows, 1,349 mammal rows, 786 mammals complete for gestation + maturity + maximum longevity (785 non-human mappings to human).
- [x] 3,140 prespecified mapping rows generated across maturity and 25/50/75% maximum-lifespan positions.
- [x] Official descriptive disagreement summary recorded in `process/PILOT0_OFFICIAL_RESULTS.md`.
- [x] Reproducible summarizer added; artifact/source hashes recorded.\n- [x] Pilot 1 independent demography benchmark completed on 88 overlapping mammals.\n- [x] Péron et al. 2019 published S5 mortality parameters vendored with DOI and SHA-256 provenance.\n- [x] Pilot 1 now consumes the canonical successful Pilot 0 artifact rather than redownloading AnAge.\n- [x] Paired 10,000-resample bootstrap added for cross-method MAD differences.\n- [x] A10 significantly favors A1 concentration; juvenile-stage end modestly favors A3; senescence onset does not clearly separate A1/A3.\n- [x] Full Pilot 1 result frozen in `process/PILOT1_DEMOGRAPHY_RESULTS.md`.

## Primary novelty claim to test

Not "the first cross-species age translator."

Instead:

> A systematic benchmark of competing age-equivalence constructs across many mammalian species, explicitly testing whether developmental, life-history, demographic and molecular age mappings agree, where they fail, and whether any one-dimensional latent age scale is empirically defensible.

This remains a provisional novelty claim until the closest-prior-work search is completed to saturation.

## Current gates

### GATE N — novelty
**PROVISIONAL PASS.**

Strong adjacent work exists, especially Translating Time and pan-mammalian epigenetic clocks, but the present search has not identified a study whose primary objective is to benchmark several mechanistically distinct age-equivalence definitions against each other across a broad mammalian sample while quantifying disagreement and cycle consistency.

### GATE D — open-data feasibility
**LIKELY PASS.**

Core sources are public or have public derived tables/code:
- AnAge/HAGR;
- Myhrvold amniote life-history data;
- Mammalian Methylation Consortium code/data resources;
- MammalMethylClock;
- Translating Time / published supplementary datasets;
- published mortality-curve parameter supplements;
- COMADRE for open demographic matrices.

Species360 raw records are useful but are not required for V1.

### GATE M — measurement validity
**OPEN.**

The main risk is construct invalidity: maximum lifespan, sexual maturity, mortality hazard, organ development and DNA methylation need not represent the same latent quantity. This is the central empirical question, not merely a nuisance.

### GATE P — phylogeny
**OPEN but specified.**

Species are not independent observations. Phylogenetic block cross-validation and phylogenetic models are required before comparative trait interpretations.

## Next execution queue

1. Acquire Januel et al. 2026 Translating Time Table S1 plus Dataset 1 authors' R script.
2. Reproduce the human/cat/mouse/chimpanzee event-scale model from published supplementary data.
3. Build held-out-event evaluation against A1/A3 without training on those events.
4. Split event performance by developmental / adult / aging phases and data type.
5. Expand event-scale coverage using earlier Translating Time mammal/primate datasets.
6. Only after event-scale validation, add published molecular/epigenetic clocks.
7. Add Myhrvold and phylogenetic tree integration before broad trait-level inference.
4. Build a pilot species intersection with high-quality data across >=3 age axes.
5. Reproduce published Translating Time / epigenetic mappings on a small reference set.
6. Run a first disagreement atlas.
7. Freeze primary evaluation metrics and exclusion rules.
8. Add phylogeny and perform leave-one-species / leave-one-order-out validation.
9. Only then consider a learned latent-age model.

## Do not do

- Do not call maximum-lifespan fraction "biological age" by definition.
- Do not use the Animal-Age three-anchor output as ground truth.
- Do not claim the mapping with the best fit to its own training target is the "true" age.
- Do not pool developmental and senescent phases without phase diagnostics.
- Do not treat epigenetic clock accuracy for chronological age as proof of cross-species biological equivalence.
- Do not use hundreds of related species as independent replicates.
- Do not broaden to all animals until the mammal benchmark works.

## Handoff sentence

If this chat is lost, resume from this file. **ARIS4C007 is a mammalian multi-axis age-equivalence benchmark, not a new pet-age conversion formula. Novelty was narrowed after discovering 2026 whole-lifespan human-cat Translating Time work. First reproduce several existing age axes, quantify their disagreement and cycle consistency, then test whether a latent common age coordinate is defensible.**
