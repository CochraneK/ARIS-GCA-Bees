# ARIS4C007 · Data-source ledger

Last updated: 2026-09-18

| Source | Main variables | Scale noted in source | Access/use plan | V1 role |
|---|---|---:|---|---|
| AnAge / Human Ageing Genomic Resources | maximum lifespan, maturity, gestation, ageing/life-history annotations | 4,645 species / 4,671 entries in current statistics | public curated database; pin downloaded build and citation | primary life-history backbone |
| Myhrvold et al. 2015 amniote life-history database | up to 29 traits incl. maturity, gestation, weaning, longevity, mass | 21,322 birds/mammals/reptiles | CC-BY dataset; pin raw archive + checksum | trait completion / robustness |
| PanTHERIA | mammalian life history/ecology/geography | all known extant/recent mammals in original release | public research dataset | robustness + ecological covariates |
| Translating Time / Workman 2013 | homologous neurodevelopmental events | 271 events, 18 mammals in paper | public model/site + paper supplementary data/code where available | developmental/event mapping |
| Charvet et al. 2023 | anatomy/behavior/transcription across primates | 573 time points, human + 8 nonhuman primates | public supplementary data | lifespan event mapping subset |
| Januel et al. 2026 human-cat | brain, blood, bone/anatomy, behavior | 3,754 observations | inspect journal supplementary reuse/license; reproduce without redistributing restricted content | closest adjacent benchmark / cat validation |
| Mammalian Methylation Consortium | conserved mammalian CpG profiles, universal clocks | >11k age-clock samples; broader consortium >15k samples/348 species | public code/resources + data browser; record exact reusable subset | molecular axis |
| MammalMethylClock R package | coefficients and age transformations | many published mammal clocks | public software/coefficients; pin version | reproducible clock application |
| Péron et al. 2019 supplements | five age-specific mortality-curve parameters | 96 mammal species | article supplementary XLSX is public | demographic-axis pilot |
| COMADRE | animal matrix population models | hundreds of species, version-dependent | open database; pin release | secondary demographic expansion |
| Primate Aging Database | body weight, blood chemistry, hematology by age | >1.3m data points on site | follow database access/publication rules | optional physiological validation |
| Primate Life History / survival studies | individual histories/life tables | study-specific | public/controlled depending source | demographic validation |
| Dog Aging Project | longitudinal dog health/environment/medical variables | cohort/version dependent | open-data release under project terms | optional dog functional-age validation |
| Animal-Age (CochraneK) | 103-species heuristic anchors + UI | 103 species | project-owned public repo | baseline + later interactive supplement |

## Acquisition rules

1. Every raw source gets version/date/checksum where possible.
2. Do not scrape a dynamic website when an official download/archive exists.
3. Preserve original units and provenance before harmonization.
4. Do not silently replace maximum lifespan with mean/median lifespan.
5. Record captive/wild, sex, breed/strain and population context whenever available.
6. Derived tables may be committed only when source licensing permits redistribution.
7. Restricted raw data must be represented by acquisition instructions and derived non-identifying summaries, not copied into the repository.

## First low-cost acquisition target

Before molecular data:
- AnAge life-history table;
- Myhrvold life-history data;
- Péron 2019 mortality-parameter supplement;
- Translating Time event/model data.

These four sources are sufficient to test whether basic disagreement exists before investing in methylation harmonization.
