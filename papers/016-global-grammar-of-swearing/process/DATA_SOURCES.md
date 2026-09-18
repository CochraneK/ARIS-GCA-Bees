# ARIS4C016 Data Sources

## Phase 0 — canonical empirical seed

### Sulpizio et al. 2024 open data
Article: https://doi.org/10.3758/s13428-024-02376-6
Open materials/data/scripts: https://osf.io/ecr32/

Role:
- reproduce published results;
- audit lexical/category structure;
- estimate community/language variance;
- create first Taboo Fingerprints.

Status: identified; not yet materialized in ARIS4C.

## Language genealogy and geography

### Glottolog
https://glottolog.org/

Role:
- stable language identifiers;
- family classification;
- geographic metadata;
- genealogy-aware grouping/covariance.

Do not treat family labels as culture.

## Linguistic structure

### WALS
https://wals.info/

Role:
- exploratory typological covariates where coverage and feature relevance are sufficient.

Avoid large feature fishing; preregister a small subset if used confirmatorily.

## Cultural-context candidates

### World Values Survey
Role: country/population-level values for carefully aligned secondary analyses.

Constraint:
country-level values cannot be interpreted as individual speaker traits, and Phase 0 has too few countries for high-dimensional cultural regression.

### D-PLACE / Ethnographic Atlas-style resources
Role: possible society-level cultural structure for later expansion when a defensible population mapping exists.

Constraint:
do not force modern national samples onto historical ethnographic societies.

## Optional external-validity corpora

Large web/social-media corpora may be used only as secondary validation of usage/register. They are not substitutes for speaker-elicited taboo judgments because platform demographics, moderation and censorship directly affect observed profanity.
