# Pilot 9 next deep-coding strategy

## Why a cell-level queue

Pilot 9 increased A–F coverage to:

- A 16/79
- B 18/79
- C 25/79
- D 17/79
- E 16/79
- F 31/79

The architecture-balanced diagnostic shows that simply increasing total observed cells does not monotonically improve threshold/weakest-link recoverability. Uneven missingness can make the architecture signatures harder to distinguish.

Therefore the next wave is scheduled by **missing taxon × module cells**, not by a single list of species.

## Queue size

There are **351 currently unobserved A–F cells**:

- 118 in the 21 Tier-1 additions not yet deep-coded;
- 128 backfill cells in the retained 29;
- 105 second-pass cells among the 29 Pilot-9 taxa already given a standardized first pass.

## Priority logic

The score combines:
1. current module coverage deficit;
2. within-taxon A–F sparsity;
3. cohort stage;
4. a modest architecture-discrimination boost for A/B/E.

The score is a **search-allocation score, not a biological-importance score**.

## Bundle rule

Do not exhaust a single module globally before moving to the next one.

Work in balanced bundles:
- **ABE core** — generative cognition, social transmission, persistent externalization;
- **CDF support** — communication, manipulation/embodiment, social architecture.

Within each taxon batch, try to advance both bundles. The v3 simulation showed that single-column completion can fail to improve threshold recovery, whereas balanced multi-module completion performs better.

## Cohort rule

Do not choose between “finish remaining 21” and “backfill old 29” as mutually exclusive strategies.

Use interleaved batches:
- remaining21 first-pass cells;
- retained29 systematic backfill;
- second-pass searches on already-screened taxa when they target especially discriminating A/B/E gaps or tested-negative evidence.

## Evidence rule

A search cell closes as one of:
- positive / measured / proxy with source and claim limit;
- tested negative at the subindicator level;
- ambiguous/disputed;
- not located after the specified search round.

**Not located is never biological absence.**

## Gate

Confirmatory necessary/sufficient inference remains blocked until:
- A–F coverage is substantially more balanced across taxa and modules;
- O1–O7 is expanded beyond the current theory/calibration cohorts;
- empirical values replace binary evidence-presence masks;
- phylogenetic/measurement uncertainty is propagated;
- architecture recovery is rerun on observed values, not just simulated latent traits.
