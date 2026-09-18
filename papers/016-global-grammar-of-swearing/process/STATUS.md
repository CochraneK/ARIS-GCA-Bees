# ARIS4C016 Status

Updated: 2026-09-18

## Stage

**Phase 0 measurement, genealogy, and repeated-item modeling.**

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
- orthogonal multi-axis taboo ontology v0 and JSON schema added;
- conservative label harmonization v0 quantified;
- 18 community samples linked to 13 Glottolog language IDs / 5 top-level families;
- genealogy/identification limits documented;
- English repeated-item community-variation diagnostic and item-fixed-effects model completed;
- stratified dual-coder reliability protocol and deterministic audit sampler implemented;
- phonology feasibility audit completed and external G2P/PHOIBLE replication plan specified;
- naïve semantic-fingerprint construction tested and rejected as measurement-biased.

## Immediate next gates

1. Execute independent dual coding on the deterministic stratified ontology audit sample.
2. Estimate axis- and label-level reliability; adjudicate only after freezing A/B labels.
3. Re-code enough lexical items to construct the first measurement-corrected semantic fingerprints.
4. Extend the repeated-item model with ontology interactions and non-taboo dimension controls.
5. Build the external pronunciation/G2P validation layer for the preregistered approximant replication.
6. Freeze confirmatory semantic and phonological hypotheses.
7. Design the expanded crossed language × country sample to repair Phase-0 identification limits.

## Current blockers

- raw third-party OSF data are intentionally not vendored because the OSF project page reports no project-level license; reproducible URLs/GUIDs/hashes are recorded instead;
- 17 countries are too few for aggressive country-level cultural regression;
- many language and country effects are confounded in the existing sample;
- semantic translation equivalence requires explicit audit;
- independent/native-speaker coding has not yet been executed;
- the existing flat category scheme cannot identify semantic fingerprints for many insult/slur rows;
- expansion sampling and ethics review are not yet frozen.

## Promotion rule

Do not promote this project beyond research-design/pilot status until the public dataset is reproduced and the variance decomposition is executable end-to-end.
