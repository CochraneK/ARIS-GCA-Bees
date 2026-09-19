# STATUS — ARIS4C007

**Last updated:** 2026-09-19  
**State:** `PILOT3B_METADATA_PASS / PILOT3C_SMOKE_ENGINEERING`  
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
- [x] Reproducible summarizer added; artifact/source hashes recorded.
- [x] Pilot 1 independent demography benchmark completed on 88 overlapping mammals.
- [x] Péron et al. 2019 published S5 mortality parameters vendored with DOI and SHA-256 provenance.
- [x] Pilot 1 now consumes the canonical successful Pilot 0 artifact rather than redownloading AnAge.
- [x] Paired 10,000-resample bootstrap added for cross-method MAD differences.
- [x] A10 significantly favors A1 concentration; juvenile-stage end modestly favors A3; senescence onset does not clearly separate A1/A3.
- [x] Full Pilot 1 result frozen in `process/PILOT1_DEMOGRAPHY_RESULTS.md`.
- [x] Januel et al. 2026 Table S1 (3,754 observations) and authors' Dataset 1 R code acquired from PMC AWS and vendored with hashes.
- [x] Pilot 2 strict observed-event benchmark built: 945 held-out source→human event rows across 799 Timepoint clusters.
- [x] Timepoint-cluster bootstrap and species-stratified bootstrap implemented.
- [x] A4 Januel-style pairwise smooth spline evaluated by leave-one-Timepoint-out rather than training fit.
- [x] Three-method benchmark completed: A1 median fold error 1.75×; A3 1.69×; A4-LOTO 1.22× overall.
- [x] A4 does not universally dominate: chimpanzee A3≈A4; postnatal 0–2 years clearly favors A3.
- [x] Full Pilot 2 result frozen in `process/PILOT2_EVENT_RESULTS.md`.
- [x] Pilot 3 molecular-axis protocol frozen in `process/PILOT3_MOLECULAR_PLAN.md`.
- [x] Pilot 3A Universal Clock 2/3 coefficients and linear predictors independently reproduced against MMC v3.0.0 on 50 official bottlenose-dolphin examples.
- [x] MammalMethylClock v1.1.0 coefficient tables pass parity to <1e-6, but its released Clock-3 inverse wrapper fails parity (median 8.78 y; max 42.14 y difference from MMC reference).
- [x] MMC Clock-3 documented Lu transform reproduced to machine precision; MMC v3.0.0 is now the canonical implementation.
- [x] Additional Clock-1 reference-script indexing issue recorded and Clock 1 quarantined pending separate validation.
- [x] Full implementation audit frozen in `process/PILOT3A_CLOCK_PARITY_RESULTS.md`.
- [x] GSE223748 metadata-first audit completed: 15,043 samples, 346 species, 70 tissue labels.
- [x] Explicit pan-clock training membership parsed: 11,514 training / 3,529 non-training samples.
- [x] Primary independent molecular holdout frozen: 50 pan-clock-training=no samples across six Pilot-0-overlap species, all with individual IDAT pairs.
- [x] Pilot 3B result frozen in `process/PILOT3B_METADATA_RESULTS.md`.
- [x] Pilot 3C bounded smoke set frozen at 10 samples / 6 species (two species have only one eligible independent holdout sample).
- [x] Pilot 3C SeSAMe 1.26.0 environment, Pilot0/Pilot3B artifact resolution, raw GEO IDAT acquisition, and MMC v3.0.0 Clock2/3 coefficient retrieval all independently reached PASS in CI.
- [x] Latest pre-fix smoke run `35424097947` downloaded all 20 IDAT files successfully; failure occurred only in the post-download filename count check.
- [x] Root cause isolated: Python TSV writer emitted CRLF; Bash retained trailing `\r` in the final `filename` field, so downloaded filenames carried a hidden carriage return and no longer matched `*.idat.gz` / SeSAMe manifest paths.
- [x] CRLF fix committed: Pilot 3C TSV manifests now force LF via `lineterminator="\n"`; R readers additionally `trimws()` filenames.
- [x] Current corrected smoke rerun: GitHub Actions run `35433019496` (triggered from commit `953220c837165d24d1e2f3e0e654fa7fc382e504`).
- [x] Full 50-sample workflow is already chained to run automatically only after a successful smoke.

## Pilot 3C engineering checkpoint

- **Smoke sample:** 10 samples across 6 species: *Delphinapterus leucas* 2, *Didelphis virginiana* 1, *Mus musculus* 2, *Orcinus orca* 2, *Rattus norvegicus* 2, *Vombatus ursinus* 1.
- **Primary full holdout:** 50 samples across the same six species, all explicitly `panmammalianclocktrainingset = no`.
- **Normalization:** SeSAMe `SHCDPB`, compressed GEO `.idat.gz` read directly, `collapseToPfx=TRUE`.
- **Clock implementation:** MMC v3.0.0 Clock 2/3 coefficients and inverse transforms are canonical.
- **Required QC:** >=95% required CpG coverage for both clocks in every smoke sample before scaling.
- **Transform separation:** full analysis stores Clock2/3 molecular linear predictors before applying life-history inverse transforms.
- **Trait vintages:** primary reproduction uses MMC v3.0.0 clock-era `anage49.csv`; current Pilot0 AnAge is a database-version sensitivity analysis.
- **Current run:** `35433019496`.
- **Full DAG:** `.github/workflows/007-pilot3c-full-molecular.yml` starts only after a successful smoke.

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

1. Complete the corrected 10-sample / six-species Pilot 3C raw-IDAT smoke test (`35433019496`).
2. Require >=95% universal-clock CpG coverage and valid Clock 2/3 predictions in every smoke sample.
3. If smoke passes, expand the identical SeSAMe/MMC pipeline to all 50 independent non-training holdout samples.
4. Compare Clock 2/3 chronological prediction residuals by species, tissue and life stage.
5. Add molecular coordinates to the cross-method disagreement benchmark with explicit target-transform circularity labels.
6. Use the 74-sample Pilot-2-overlap molecular set only for event-conditioned triangulation, never as the primary independent holdout.
7. After molecular feasibility, add Myhrvold + mammalian phylogeny for broad trait-level inference.
8. Build the first multi-axis disagreement atlas.
9. Freeze phylogenetic leave-one-order-out validation before any latent-age model.

## Do not do

- Do not call maximum-lifespan fraction "biological age" by definition.
- Do not use the Animal-Age three-anchor output as ground truth.
- Do not claim the mapping with the best fit to its own training target is the "true" age.
- Do not pool developmental and senescent phases without phase diagnostics.
- Do not treat epigenetic clock accuracy for chronological age as proof of cross-species biological equivalence.
- Do not use hundreds of related species as independent replicates.
- Do not broaden to all animals until the mammal benchmark works.

## Handoff sentence

If this chat is lost, resume from this file. **Pilots 0–2, Pilot 3A implementation parity, and Pilot 3B metadata/holdout selection are complete. Pilot 3C has a frozen 50-sample/6-species pan-clock-training=no holdout and a 10-sample/6-species smoke. The latest pre-fix run downloaded all IDATs but failed because CRLF in `download_manifest.tsv` polluted Bash filenames; that bug is fixed in Git and corrected run `35433019496` is the current gate. If smoke passes, the full 50-sample workflow should auto-start. MMC v3.0.0 remains canonical; keep molecular linear predictors separate from Clock2/3 life-history inverse transforms and report clock-era vs current-AnAge trait sensitivity.**
