# PILOT 2 RESULTS · ARIS4C008

## Purpose

Pilot 2 adds energetic and life-history constraints to the culture/cognition evidence matrix and resolves the largest taxonomy problem identified in Pilot 1.

## AnimalTraits

The frozen AnimalTraits v1.0.7 CSV was parsed directly rather than manually transcribed.

For the v1 seed labels:
- 11 / 25 pilot taxon labels had at least one exact or explicit exemplar match;
- 12 matched species/exemplar rows were produced;
- the resulting file preserves observation counts, medians, ranges and units separately for body mass, brain size and metabolic rate.

A blank-value bug in the first aggregation attempt was detected immediately: JavaScript would coerce an empty string to numeric zero. The erroneous summary was replaced. The final extract treats blanks as missing.

Files:
- `data/animaltraits_pilot_summary.csv`
- `code/ingest_animaltraits.py`

## AnAge

The AnAge bulk archive was downloaded and parsed as tabular data. The fetched stable bulk file contained 4,645 data rows.

The normalized v1 extract contains 24 actual species rows, including exact records for many core taxa and explicit genus/family exemplars for unresolved labels.

Files:
- `data/anage_pilot_summary.csv`
- `process/ANAGE_PILOT_RESULTS.md`
- `code/ingest_anage.py`

## Integrated matrix v1

`data/pilot_matrix_v1.csv` joins:
- ACDB cultural-behaviour coverage;
- scoped literature evidence counts;
- AnimalTraits body/brain/metabolic coverage;
- AnAge maturity, gestation, weaning, interbirth interval, longevity, mass and metabolic fields.

Current v1 coverage:
- 25 seed taxon labels total;
- 22 have a longevity value through exact or explicit exemplar matching;
- 10 have brain-size records in AnimalTraits;
- 6 have at least one metabolic-rate source across AnimalTraits/AnAge;
- 19 have an exact-species energetic or life-history route.

These are coverage statistics, **not biological scores**.

## Taxonomic resolution

Genus/family labels are not suitable as terminal units in phylogenetic comparative models.

`data/pilot_taxa_v2.csv` therefore resolves/splits:
- `Pongo spp.` → `Pongo abelii`, `Pongo pygmaeus`;
- `Gorilla spp.` → `Gorilla gorilla`, `Gorilla beringei`;
- `Sapajus spp.` → `Sapajus libidinosus`;
- `Macaca spp.` → `Macaca fuscata`;
- `Callitrichidae` → `Callithrix jacchus`, `Leontopithecus rosalia`;
- adds `Tursiops aduncus` alongside `T. truncatus` so the Shark Bay tool-culture evidence is not silently assigned to the wrong bottlenose-dolphin species.

The resulting exact-taxonomy v2 seed has 29 taxa before model-discriminating calibration taxa are added.

## Main lesson

The life-history hypothesis is now empirically tractable rather than rhetorical. There are already clear comparative dissociations: teaching, socially transmitted solutions, cultural traditions and sophisticated manipulation occur across taxa with very different maturation schedules and maximum lifespans.

The next task is not to proclaim one necessary condition, but to quantify module values consistently and test interactions after research-effort and phylogenetic correction.
