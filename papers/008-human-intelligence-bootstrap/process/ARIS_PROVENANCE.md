# ARIS provenance · Paper 008

## Frozen engine

- Upstream: `wanshuiyin/Auto-claude-code-research-in-sleep`
- Release: **v0.4.26**
- Tag commit: **951654847b015585385b2448c5667dcd04e7b56b**
- Upstream release published: **2026-09-16**
- Provenance frozen for Paper 008: **2026-09-18**

This commit was resolved directly from the upstream Git tag. It is not inferred from the ARIS4C lock file alone.

## Relationship to ARIS4C008 work

Paper 008 underwent substantial ARIS4C-guided design work before the formal full engine run:
- outcome ontology and candidate-condition ontology;
- real ACDB extraction;
- AnimalTraits and AnAge integration;
- model-recoverability stress tests;
- OpenTree taxonomic/phylogenetic reconciliation;
- OpenAlex research-effort proxy;
- closest-prior-work/novelty review;
- hominin temporal falsification layer;
- neural harmonization/falsification layer.

These pilot outputs are inputs to the formal run; their provenance must not be rewritten merely because ARIS is upgraded later.

## Formal-run input manifest

The formal run should treat the following as canonical design inputs:

- `process/RESEARCH_PLAN.md`
- `process/OUTCOME_CODEBOOK.md`
- `process/DESIGN_GATES.json`
- `process/CLOSEST_PRIOR_WORK.md`
- `process/NOVELTY_GATE.md`
- `process/HOMININ_TEMPORAL_LAYER.md`
- `process/NEURAL_HARMONIZATION.md`
- `process/PANEL_V2_DESIGN.md`
- `data/pilot_taxa_v2.csv`
- `data/literature_seed_evidence.csv`
- `data/openalex_research_effort_v0.csv`
- `data/opentree_taxonomy_v2.csv`
- `data/anage_pilot_summary.csv`
- `data/animaltraits_pilot_summary.csv`
- `data/neural_measurements_seed.csv`
- `data/hominin_milestones_v0.csv`
- `data/hominin_temporal_falsification_v0.csv`

## Reproducibility rule

If the upstream ARIS version changes after this date:
- Paper 008 keeps this frozen provenance for the current research cycle;
- a reconstruction using a newer ARIS version must be recorded as a new run/revision rather than silently replacing this provenance.

## Current execution status

**Engine provenance: frozen.**
**Full ARIS synthesis run: not yet claimed complete.**

The provenance gate concerns reproducibility of the engine version; it does not by itself imply that every confirmatory dataset or model has been completed.
