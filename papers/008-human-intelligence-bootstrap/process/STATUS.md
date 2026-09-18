# STATUS · ARIS4C008

Updated: 2026-09-18

## Canonical question

**Which configurations of cognitive, social, embodied, life-history, energetic, ecological, demographic and externalized-information capacities are candidate necessary, enabling, bottleneck, amplifying or jointly sufficient components for transitions toward open-ended cumulative intelligence?**

The project does not assume a fixed evolutionary “skill-point budget” and does not define intelligence by resemblance to humans.

## Current stage

**Pilot 8 · configuration-diverse screening and Tier-1 deep-coding design.**

Confirmatory necessary/sufficient inference remains **BLOCKED**, but the design is now substantially closer to an identifiable study.

## Sampling architecture

### Retained deep seed
- 29 exact species from Pilot 7.
- 29/29 have an exact-species evidence route.

### Broad screening pool
- **238 operational taxa** in `screening_pool_expanded_v1.csv`.
- Roles include ACDB/ASNR source candidates, matched ordinary controls, underrepresented-clade controls and theory-discriminating counterexamples.
- Absence from ACDB/ASNR is never interpreted as trait absence.

### Tier-1 staged expansion
- retain the original 29;
- add **50 new taxa**;
- resulting staged panel: **79 taxa**.

The new 50 comprise:
- 14 theory-discriminating candidates;
- 15 data-rich underrepresented-clade calibration taxa;
- 10 same-family/body-mass-matched ordinary controls;
- 11 data-driven source candidates.

This 79 is a deep-coding wave, not a claimed universally optimal final sample size.

## Taxonomy

The canonical 238-taxon pool was rerun through OpenTree 3.7 with approximate matching disabled:

- 222 clean non-synonym self species matches;
- 15 explicit synonym / operational-taxonomy cases;
- 3 multi-match queries resolved by a unique non-synonym self match;
- 1 OpenTree exact-TNRS gap: *Serracutisoma proximum*, retained with a documented legacy OTT crosswalk.

Domestic dog/chicken and other below-species/duplicate operational forms are prevented from becoming fake independent phylogenetic terminals.

## Low-cost screening layer

`build_screening_features.py` rebuilds the 238-taxon screen from standardized public sources.

Current matching:
- AnAge: 142 / 238;
- AnimalTraits: 80 / 238;
- EltonTraits: 179 / 238;
- PanTHERIA: 118 / 238;
- ASNR network metrics: 87 / 238.

Proxy-block coverage:
- F network: 87;
- G life history: 139;
- H neural/energetic: 101;
- I ecology: 179;
- J demography: 89.

Database presence affects **feasibility only**, never biological configuration distance.

## Tier-1 79-taxon empirical starting mask

Current observed/proxy coverage:

| Module | Coverage |
|---|---:|
| A · generative cognition | 9 / 79 |
| B · social transmission | 16 / 79 |
| C · communication | 11 / 79 |
| D · manipulation / embodiment | 8 / 79 |
| E · persistent externalization | 10 / 79 |
| F · social architecture | 21 / 79 |
| G · life history / learning opportunity | 60 / 79 |
| H · energetics / neural budget | 55 / 79 |
| I · ecological challenge / opportunity | 53 / 79 |
| J · demography / cultural population | 41 / 79 |

The dominant empirical gap is now clearly A–E, not basic ecology/life history.

## Theory-counterexample seed

The 14 theory-discriminating candidates now have 21 source-traceable exact-species module evidence rows.

Examples of deliberate dissociations include:
- scrub-jay future planning;
- sea-otter habitual stone tool use;
- beaver persistent dam construction;
- zebra-finch and sac-winged-bat vocal learning;
- naked-mole-rat culturally transmitted vocal dialect;
- cleaner-fish social learning;
- wolf and African-wild-dog cooperation;
- leaf-cutter-ant persistent cultivation/division of labour.

These are candidate anti-sufficiency contrasts, not automatic proofs of insufficiency.

## Recoverability · methodological correction

### Legacy diagnostic

The Pilot-7/early Pilot-8 simulation let a flexible three-feature “interaction” model compete with simpler models and let threshold share features with weakest-link. Its low complete-data recovery therefore mixed:
- panel/missingness limitations;
- genuine signature overlap;
- unequal model flexibility.

Those results remain archived for audit but are **not the final gate definition**.

### Architecture-balanced v2 gate

The primary static recoverability diagnostic now gives additive, weakest-link and threshold equal fitted complexity: each is a fixed one-dimensional architecture signature with intercept + slope.

Dynamic interaction/feedback is retained as a substantive hypothesis but must be modeled with explicit temporal/network structure rather than as a static catch-all polynomial.

V2 recovery:

| Scenario | Additive | Weakest | Threshold |
|---|---:|---:|---:|
| 29 current | 0.642 | 0.478 | 0.386 |
| 79 current | 0.768 | 0.414 | 0.448 |
| new 50 A–F complete | 0.994 | 0.526 | 0.310 |
| all 79 A–F complete | 1.000 | 0.742 | 0.550 |
| 79 × 10 complete, random configurations | 1.000 | 0.850 | 0.748 |
| 79 × 10 complete, oracle configuration geometry | 1.000 | 1.000 | 0.915 |

The oracle row is an upper bound using latent architecture signatures and is not directly implementable before measurement.

## What the v2 gate says

1. **79 taxa can be enough in principle** for the primary static architecture question.
2. Merely adding taxa without balanced module coding is not enough.
3. Deep-coding only the new 50 leaves old-panel A–F and G–J imbalance; it does not solve identifiability.
4. After A–F are complete, J and H are high-priority remaining gaps; G is no longer a major bottleneck.
5. Configuration geometry still matters strongly: random complete 79 < deliberately discriminating complete 79.

## Current design gates

### Passed
- ARIS provenance freeze.

### Provisional pass
- outcome codebook;
- condition ontology;
- research-effort framework;
- screening taxonomy;
- phylogenetic topology;
- broad screening pool construction;
- Tier-1 selection algorithm;
- hominin temporal layer;
- novelty boundary;
- neural harmonization.

### BLOCKED
- **confirmatory model recoverability / minimal necessary-sufficient configuration inference.**

## Unblock plan

1. Deep-code A–F for the 50 Tier-1 additions.
2. Backfill A–F gaps in the original 29, rather than treating the old panel as finished.
3. Prioritize standardized J and H expansion; I next; G last among G–J.
4. Code O1–O7 outcomes independently for all Tier-1 taxa.
5. Search explicitly for tested-negative evidence, especially in ordinary/underrepresented calibration taxa.
6. Add dated/justified phylogenetic branch lengths.
7. Recompute empirical configuration geometry after A–J values exist.
8. Rerun the architecture-balanced gate on observed data and missingness.
9. Model interaction/feedback separately using temporal/network structure.
10. Only then estimate candidate necessary/sufficient sets.

## Current scientific assessment

**Framing: strong. Counterexample design: strong. Data infrastructure: advanced. Tier-1 behavioral coding: incomplete. Confirmatory causal/configurational claims: not ready.**

The project can already reject several naive single-factor stories, but it cannot yet state the minimal sufficient or necessary architecture of human-like open-ended cumulative intelligence.
