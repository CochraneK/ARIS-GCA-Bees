# Code — ARIS4C005

## Executable pipeline

### Denominator / detected lower bound

- `build_universe.py` — OpenAlex annual target-universe counts + query provenance.
- `classify_retractions.py` — conservative Retraction Watch screening flags; never an adjudicated truth label.
- `summarize_retractions.py` — event-row vs unique-work public-safe correction snapshot.

Primary Pilot A denominator:

`OpenAlex core + article|review + publication years 2000–2025`.

### Pilot B sampling / adjudication

- `build_pilot_b_seed.py` — real OpenAlex population-random sample + stratified Retraction Watch enrichment with exact first-order inclusion probabilities/design weights.
- `pilot_b_sample.py` — generic two-phase probability-aware sampling utility.
- `make_adjudication_packet.py` — blinded reviewer packet + manager-only detector/sampling linkage.
- `make_micro_pilot.py` — 60-work balanced cross-domain protocol stress-test; explicitly not a prevalence sample.
- `merge_adjudications.py` — fail-closed vocabulary QA, reviewer/linkage merge and disagreement reporting.
- `calibrate_detectors.py` — design-weighted calibration diagnostics: sensitivity/specificity/PPV/NPV, missingness and Kish effective sample size.

Current real Pilot B seed:

- target years: 2015–2020;
- target denominator: **38,451,124** core article/review works;
- population-random sample: **600**;
- resolved Retraction Watch enrichment: **739**;
- unique seed: **1,339**;
- micro-pilot: **60 works / 120 double-coded assignments**.

These are sampling-infrastructure counts, **not severe-failure prevalence**.

### Scenario / later burden modules

- `scenario_model.py` — transparent Monte Carlo/Fermi scenarios tagged `SCENARIO_NOT_EMPIRICAL_ESTIMATE`.

Next empirical modules:

```text
citation_dependence.py
contamination_graph.py
knowledge_ghost_half_life.py
latent_prevalence.py
rly_cost.py
innovation_delay.py
sleeping_beauty.py
```

Semantic contamination may progress while human Pilot B adjudication is pending; latent prevalence may not.

---

## Core sampling formula

For a work reachable through independent population-random and enrichment mechanisms:

`pi_i = 1 - (1 - p_random)(1 - p_enrich,s)`

Primary design weight:

`w_i = 1 / pi_i`

Enrichment-only raw sample proportions must never be interpreted as population prevalence.

---

## Validation

GitHub Actions compiles all Python sources and runs invariant unit tests.

Protected invariants include:

- plagiarism is not automatically false science;
- honest major error is not misconduct;
- investigation alone is not misconduct;
- paper-mill signal is not automatically E1-S;
- unresolved/indeterminate adjudications are not silently recoded as negatives;
- enrichment samples retain explicit inclusion probabilities/design weights;
- reviewer packets hide detector/sampling metadata;
- invalid adjudication vocabularies fail closed;
- the micro-pilot spans available broad domains within signal groups;
- scenario outputs remain labelled non-empirical.

---

## Data governance

See:

- `../process/ADJUDICATION_PROTOCOL.md`
- `../process/PILOT_B_DATA_CONTRACT.md`
- `../process/PILOT_B_SEED_RESULTS.md`
- `../data/adjudication_template.csv`

The canonical public repository stores aggregate provenance/results. Row-level adjudication seed artifacts stay outside the public tree to avoid publishing an unretracted-author suspicion list.

No nationality, institution, language, journal reputation or coauthor network may function as a primary suspicion prior.
