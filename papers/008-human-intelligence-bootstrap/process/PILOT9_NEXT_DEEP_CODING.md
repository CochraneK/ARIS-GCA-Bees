# Pilot 9 next deep-coding strategy

Updated: 2026-09-19

## Current state

All 50 Tier-1 additions have completed standardized A–F first-pass coding. The old “remaining21 first pass” task is finished.

Current A–F coverage in module_evidence_state_tier1_v2.csv:

- A 21/79
- B 22/79
- C 34/79
- D 18/79
- E 17/79
- F 32/79

There are **330 currently unobserved A–F cells**.

## Current queue

Use data/deep_coding_cell_queue_v2.csv.

- **128** cells: retained29 systematic backfill.
- **202** cells: new50 targeted second pass.

The queue score allocates literature-search effort only. It is **not a biological-importance score**.

## Why cell-level balancing matters

Pilot-9 recoverability diagnostics showed that raw coverage can increase while threshold recovery worsens if missingness becomes more geometrically unbalanced.

Therefore:
- do not finish one module globally before the others;
- do not choose “old29 only” versus “new50 only” as mutually exclusive strategies;
- interleave taxon × module cells.

## Bundle rule

Work in balanced bundles:

### ABE core
- A generative cognition
- B social transmission
- E persistent externalization

### CDF support
- C communication
- D manipulation / embodiment
- F social architecture

ABE has high architecture-discrimination value, but it must not crowd out CDF.

## Search protocol

For each cell:

1. scientific-name search;
2. common-name fallback if indexing is weak;
3. current-name / synonym crosswalk where taxonomically justified;
4. exact-species focal-paper verification;
5. record one of:
   - positive / measured;
   - positive proxy with claim limit;
   - measured context;
   - tested negative at a named subindicator;
   - ambiguous / disputed;
   - not located after the specified round.

Near-neighbour results stay excluded.

**Not located is never biological absence.**

## Next execution order

1. Start with high-ranked retained29 backfill cells, but process them in ABE/CDF bundles.
2. Interleave high-ranked new50 second-pass cells after each retained29 bundle.
3. Give special attention to E/D/A/B because they remain the sparsest, while preserving module balance.
4. Keep a tested-negative search track in parallel.
5. After each meaningful balanced batch, rebuild the v2 queue from the current matrix.

## Outcome workstream

In parallel, expand O1–O7 to the full 79.

Do not infer outcomes from condition modules. Outcome coding must be independent.

## Recoverability rule

tier1_recoverability_v3.csv is an interim design result produced before final new50 first-pass closure.

Rerun the architecture-balanced diagnostic after balanced backfill milestones. The final scientific gate must use empirical/latent module values with uncertainty, not binary evidence-presence masks.

## Gate to full necessary/sufficient analysis

Do not proceed to confirmatory candidate necessary/sufficient sets until:
- A–F are substantially more balanced;
- O1–O7 covers all Tier-1 taxa;
- J/H coverage is improved;
- phylogenetic timing / branch lengths are defensible;
- measurement uncertainty is propagated;
- architecture recovery is acceptable on the actual observed-value dataset.
