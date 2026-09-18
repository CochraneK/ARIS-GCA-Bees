# PILOT 1 RESULTS · ARIS4C008

## What was actually executed

Pilot 1 moved 008 beyond conceptual design by integrating a real cross-taxonomic culture database, building an evidence matrix, expanding source-traceable comparative evidence and stress-testing the proposed causal architecture models.

## 1. Animal Culture Database extraction

From the published ACDB v0.1 tables:

- 61 species were present in the release;
- 116 group records were parsed;
- 129 behaviour rows were parsed;
- 13 ARIS4C008 pilot species matched directly by canonical name;
- those matches contributed 32 groups and 42 cultural-behaviour records.

The extraction is stored in:
- `data/acdb_pilot_species.csv`
- `data/acdb_pilot_behaviors.csv`

### Important inference

ACDB is an evidence source, **not a complete animal-culture census**. Non-coverage is therefore treated as missing/not-yet-covered, never as a biological zero.

## 2. Literature evidence seed

The source-traceable evidence table now contains 24 rows spanning:
- great apes;
- capuchins and macaques;
- callitrichids;
- corvids and parrots;
- pigeons;
- cetaceans;
- elephants;
- octopus;
- social insects;
- meerkats;
- humans as the target-theory reference.

Every row records an evidence scope:
- exact species;
- genus exemplar;
- family exemplar;
- clade comparative.

This prevents evidence from a related species being silently promoted to an exact-species measurement.

## 3. Current taxon coverage

Out of 25 seed taxa:
- 14 have exact-species literature seed rows;
- 5 more have exact-species ACDB records;
- 5 rely on genus exemplars;
- 1 relies on a family exemplar.

Primary-matrix expansion can therefore begin for 19 taxa. Six need taxonomic resolution before confirmatory use.

## 4. First evidence matrix

`data/pilot_matrix_v0.csv` records, for each seed taxon:
- ACDB behaviour count;
- exact and exemplar literature-row counts;
- evidence-row counts by currently populated modules;
- whether life-history and energetics joins are pending;
- whether research effort has been quantified;
- current confirmatory eligibility.

It deliberately does **not** convert evidence counts into an "intelligence score".

## 5. Mechanism recoverability

The toy simulation compared additive, weakest-link and threshold-generating systems under measurement error and missingness.

Main lesson: famous high-cognition taxa are a poor sample for distinguishing mechanisms because their trait configurations are too correlated. Selecting taxa for maximum disagreement among the competing models improves identification, especially for threshold and weakest-link mechanisms.

The simulation is reproducible in:
- `code/simulate_model_recoverability.py`
- `data/model_recoverability_summary.csv`

## 6. Design change produced by Pilot 1

The next panel is not "more smart animals".

It is a **model-discriminating comparative panel** with deliberate counterexamples and calibration taxa. See `process/PANEL_V2_DESIGN.md`.

## 7. What Pilot 1 does not establish

Pilot 1 does not establish:
- a necessary condition for human intelligence;
- a sufficient condition;
- which living animal is "closest to humans";
- a probability that another lineage will evolve human-like intelligence;
- that any candidate module is causal.

Those are later-stage hypotheses to be tested after exact-species, phylogenetic, missingness and research-effort gates are passed.
