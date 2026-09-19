# ARIS4C007 · Research context

## Project

**Are Animal Years Comparable? Benchmarking Cross-Species Biological Age Equivalence Across Mammals**

## Compact scope

A multi-axis mammalian benchmark asking whether defensible definitions of cross-species equivalent age converge on one scalar biological-time coordinate or instead define systematically different developmental, life-history, demographic and molecular notions of "same age."

Completed evidence layers:
- Pilot 0 deterministic life-history mappings;
- Pilot 1 independent demographic-event benchmark;
- Pilot 2 strict held-out homologous-event benchmark;
- Pilot 3A Universal Clock implementation/parity audit;
- Pilot 3B GSE223748 metadata audit and independent molecular-holdout freeze.

Current layer:
- Pilot 3C raw-IDAT molecular validation, beginning with a 10-sample / 6-species smoke and then a frozen 50-sample independent non-training holdout.

## Important current scientific result pattern

Pilot 2 shows that an event-rich leave-one-Timepoint-out mapping (A4) is substantially more accurate overall than simple life-history mappings, but does not universally dominate: performance differs by species and life stage. This supports the paper's core premise that cross-species age equivalence may be multi-dimensional rather than a unique ratio.

## Molecular caution

Universal Clock 2 and 3 are useful molecular measurements, but their training targets already encode life-history assumptions:
- Clock 2: maximum-lifespan relative-age target;
- Clock 3: gestation/maturity log-linear target.

Therefore independent-sample prediction is evidence of molecular generalization, **not** independent validation that A1/A3 are the uniquely correct biological-age constructs.

## Domain

comparative biology / geroscience / life-history evolution / computational biology

## Working tags

ARIS, ARIS4C, comparative aging, biological age, cross-species translation, epigenetic clocks, life history, senescence, Animal-Age

## Construct / claim discipline

Read `DECISIONS.md`, `process/STATUS.md`, `process/PILOT3A_CLOCK_PARITY_RESULTS.md`, `process/PILOT3B_METADATA_RESULTS.md`, and `process/PILOT4_PHYLOGENY_PLAN.md` before changing construct definitions or claim strength.

## Where to continue

Start from `AGENT_HANDOFF.md`, then check GitHub Actions run `35433019496`. If it has completed, update the handoff state before doing anything else.
