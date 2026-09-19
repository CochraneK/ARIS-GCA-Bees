# STATUS · ARIS4C008

Updated: 2026-09-19

## Canonical question

**Which configurations of cognitive, social, embodied, life-history, energetic, ecological, demographic and externalized-information capacities are candidate necessary, enabling, bottleneck, amplifying or jointly sufficient components for transitions toward open-ended cumulative intelligence?**

The motivating question is also practical: **what makes humans unusually capable of open-ended cumulative intelligence, which conditions are necessary versus sufficient, and which nonhuman animals already share substantial subsets of the configuration?**

The project does **not** assume a fixed evolutionary “skill-point budget”, a ladder with humans at the top, or that similarity implies an evolutionary destination.

## Current stage

**Pilot 9 · all 50 Tier-1 additions have completed standardized A–F first-pass deep coding.**

Confirmatory necessary/sufficient inference remains **BLOCKED**.

The immediate work is no longer “finish the remaining21 first pass”. It is now:

1. backfill the retained 29 A–F gaps;
2. targeted second-pass searches on the new 50;
3. expand O1–O7 outcome coding to the full 79;
4. then rerun recoverability on the updated observed matrix.

## Sampling architecture

- Retained Pilot-7 seed: **29 exact species**.
- Broad screening pool: **238 operational taxa**.
- Tier-1 deep panel: **79 taxa = retained 29 + 50 additions**.
- New 50 composition: 14 theory-discriminating candidates, 15 underrepresented-clade calibration taxa, 10 matched ordinary controls, 11 data-driven source candidates.

The 79 are a staged deep-coding panel, not a claimed universally optimal final N.

## Taxonomy rule

Use exact-species evidence wherever possible.

- Current-name / synonym crosswalks are allowed only when explicitly documented.
- Near-neighbour, same-genus or same-family findings do **not** substitute for focal-species evidence.
- Scientific-name retrieval must use common-name fallback when indexing is weak (especially cetaceans).
- not_located_first_pass means retrieval failure / evidence not located, **never biological absence**.

## Tier-1 79-taxon matrix · current v2

Canonical file: data/module_evidence_state_tier1_v2.csv.

| Module | Observed / 79 | Missing |
|---|---:|---:|
| A · generative cognition | **21** | 58 |
| B · social transmission | **22** | 57 |
| C · communication | **34** | 45 |
| D · manipulation / embodiment | **18** | 61 |
| E · persistent externalization | **17** | 62 |
| F · social architecture | **32** | 47 |
| G · life history / learning opportunity | **60** | 19 |
| H · energetics / neural budget | **55** | 24 |
| I · ecological challenge / opportunity | **53** | 26 |
| J · demography / cultural population | **41** | 38 |

A–F currently contain **144 observed cells and 330 unobserved cells**.

By cohort:
- retained29 A–F: 46 observed / 174; **128 missing**;
- new50 A–F: 98 observed / 300; **202 missing**.

The dominant gaps are still A–F, especially **E, D, A and B**. For architecture discrimination, A/B/E remain a high-value bundle, but single-column completion should be avoided.

## New50 first-pass closure

All 50 additions have completed standardized first-pass A–F coding.

The last remaining21 grid is closed:
- **126/126 cells have a state**;
- **0 pending_first_pass**;
- 97 are not_located_first_pass;
- 17 positive;
- 9 positive_proxy;
- 3 measured_context.

These states are evidence states, not organism scores.

Recent exact-species examples:
- blue/gray/right whales: direct acoustic communication evidence;
- guppy: innovation, social learning, visual signalling and social-network evidence;
- common vampire bat: demonstrator-based social learning plus long-term cooperative relationships;
- three-spined stickleback: social learning plus persistent nest construction;
- bison: memory-guided foraging, acoustic communication and collective movement decision-making;
- spotted hyena: innovation, communication and cooperation, plus a directed-social-learning boundary;
- sloth bear: positive spatial-transposition evidence coexisting with failure on one novel-problem task.

## Tested-negative policy

Negative evidence is coded only when a relevant subindicator was explicitly tested and failed.

Examples now preserved:
- sloth bear: failure to spontaneously solve a specific novel problem despite social cues / relevant experience;
- three-spined stickleback: no evidence for individual recognition in the tested paradigm;
- spotted hyena: demonstrator opportunity did not increase novel technical-problem success, despite partial social effects;
- Nephila: prior experience did not increase site tenacity;
- Hyla: a specific auditory-streaming effect was not supported.

A tested negative narrows a module; it does not automatically set the whole module to zero.

## Deep-coding queue · current v2

Canonical queue: data/deep_coding_cell_queue_v2.csv.

There are **330 currently unobserved A–F cells**:
- 128 retained29 systematic backfill;
- 202 new50 targeted second pass.

The queue is for **search allocation only**, not biological importance.

Work in balanced bundles:
- **ABE core:** generative cognition, social transmission, persistent externalization;
- **CDF support:** communication, manipulation/embodiment, social architecture.

Do not exhaust one module globally before the others.

## Recoverability status

The architecture-balanced simulation framework is valid as a **design diagnostic**, not a biological power calculation.

Key lessons already established:
- taxa count alone is insufficient;
- uneven missingness can make threshold / weakest-link architectures harder to recover even when total coverage rises;
- balanced A–F completion is more useful than opportunistic single-column completion;
- configuration geometry matters strongly.

Important provenance note:
- tier1_recoverability_v3.csv was generated **before the final all-new50 first-pass closure**.
- It should therefore be treated as an interim design diagnostic.
- Do **not** describe it as the latest recovery estimate for the current v2 matrix.
- Rerun recoverability after a balanced backfill batch, and ultimately on empirical module values rather than binary evidence-presence masks.

## Outcome coding

O1–O7 is partly developed for theory and calibration cohorts but is **not yet complete for all 79 taxa**.

This remains a major blocker. Presence of A–J conditions cannot answer necessary/sufficient questions without independent outcome coding.

## G–J priority after A–F

Among remaining G–J gaps, current design logic prioritizes:
1. **J · demography / cultural population**;
2. **H · energetics / neural budget**;
3. I;
4. G last.

## Design gates

### Passed
- ARIS provenance freeze.

### Provisional pass
- condition ontology;
- outcome codebook;
- research-effort framework;
- screening taxonomy;
- broad 238-taxon pool;
- Tier-1 selection logic;
- theory-counterexample and underrepresented-calibration architecture;
- staged phylogenetic topology;
- hominin temporal layer;
- novelty boundary;
- neural harmonization.

### BLOCKED
- confirmatory minimal necessary/sufficient configuration inference.

## Unblock plan

1. Execute data/deep_coding_cell_queue_v2.csv in balanced ABE/CDF batches.
2. Backfill the retained29; do not treat Pilot 7 as finished.
3. Run targeted second-pass searches on new50 not_located_first_pass cells.
4. Expand O1–O7 outcomes to all 79 taxa, independently from condition coding.
5. Continue explicit tested-negative retrieval.
6. Expand J and H, then I/G as needed.
7. Add dated / justified phylogenetic branch lengths and propagate measurement uncertainty.
8. Replace evidence-presence masks with empirical / ordinal / latent module values.
9. Recompute configuration geometry and rerun the architecture-balanced gate.
10. Model temporal/network feedback separately from static architectures.
11. Only then estimate candidate necessary, sufficient, bottleneck or enabling sets.

## Scientific assessment

**Framing: strong. Counterexample design: strong. Data infrastructure: advanced. New50 first-pass A–F: complete. Retained29 A–F backfill / new50 second pass / full outcome coding: incomplete. Confirmatory configurational claims: not ready.**
