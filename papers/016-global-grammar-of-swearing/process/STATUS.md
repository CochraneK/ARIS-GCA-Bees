# ARIS4C016 Status

Updated: 2026-09-18

## Stage

**Phase 0 measurement audit + ontology harmonization.**

The project has entered empirical Phase 0 using the public Sulpizio et al. dataset. The current evidence is a structural/reproducibility audit, not a validated global cultural model.

## Completed

- canonical research question defined;
- novelty reframed away from a simple swear-word dictionary;
- key prior art audited;
- open Phase-0 dataset identified;
- falsification-first hypothesis hierarchy drafted;
- language-vs-culture decomposition strategy specified;
- phylogenetic pseudoreplication recognized as a primary design threat;
- public-output ethics for slurs and identity-targeting language specified;
- OSF file inventory and SHA-256 provenance frozen;
- Study-1/Study-2 CSV structure audited directly;
- cross-sample category missingness and multi-label heterogeneity quantified;
- same-language English/Spanish rating baselines recomputed;
- reproducible de-identified audit script added;
- orthogonal multi-axis taboo ontology v0 and JSON schema added.

## Immediate next gates

1. Build conservative raw-label normalization and mapping rules without overwriting source labels.
2. Create a stratified ontology-audit sample and reliability protocol.
3. Reproduce original Study-2 affective/rating baselines in our own pipeline.
4. Run measurement-aware same-language community contrasts.
5. Add Glottolog identifiers and language-family/geographic metadata.
6. Specify genealogy-aware variance/dependence models.
7. Preregister confirmatory semantic and phonological hypotheses.
8. Only after Phase 0 succeeds, design an expanded multilingual elicitation sample.

## Current blockers

- raw third-party OSF data are intentionally not vendored because the OSF project page reports no project-level license; reproducible URLs/GUIDs/hashes are recorded instead;
- 17 countries are too few for aggressive country-level cultural regression;
- many language and country effects are confounded in the existing sample;
- semantic translation equivalence requires explicit audit;
- expansion sampling and ethics review are not yet frozen.

## Promotion rule

Do not promote this project beyond research-design/pilot status until the public dataset is reproduced and the variance decomposition is executable end-to-end.
