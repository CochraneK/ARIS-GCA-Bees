# Code — ARIS4C005

## Current executable modules

### `build_universe.py`

Queries the OpenAlex Works API and writes annual target-universe counts plus query provenance.

Primary frozen definition:

`OpenAlex core + article|review + publication years 2000–2025`.

This constructs a denominator only; it does not estimate misconduct.

### `classify_retractions.py`

Maps raw Retraction Watch multi-label reasons to conservative screening variables:

- narrow E1-S;
- strong E1-M;
- strong E1-P;
- paper-mill signal;
- major-error signal;
- manual scientific/process review.

Automatic flags are screening variables, not adjudicated truth.

### `summarize_retractions.py`

Produces a public-safe aggregate snapshot:

- event rows;
- unique original-paper DOI counts;
- row-level and unique-work flag counts;
- real parsed date range;
- reason frequencies;
- provenance/checksum.

Raw Retraction Watch input is not committed.

### `pilot_b_sample.py`

Creates the two-phase Pilot B adjudication sample using independent Bernoulli/Poisson components:

1. population-random probability `p_r`;
2. detector-enrichment probability `p_e`.

Exact first-order inclusion probability:

`pi = 1 - (1 - p_r)(1 - p_e)`

Every selected paper stores `pi` and `1/pi` design weight. CLI sample-size targets are expected counts.

### `calibrate_detectors.py`

Computes design-weighted calibration diagnostics against resolved manual adjudications:

- severe-failure prevalence point estimate;
- detector sensitivity/specificity/PPV/NPV;
- detector missingness;
- Kish effective sample size;
- engineering identification gate.

This is **not** the final Bayesian latent prevalence model.

### `scenario_model.py`

Runs transparent Monte Carlo/Fermi scenarios from external parameter JSON. Every output is tagged:

`SCENARIO_NOT_EMPIRICAL_ESTIMATE`.

Scenario output cannot enter the evidence ledger as a finding without empirical calibration.

---

## Validation

GitHub Actions compiles all Python sources and runs invariant unit tests.

Current protected invariants include:

- plagiarism is not automatically false science;
- honest major error is not misconduct;
- investigation alone is not misconduct;
- paper-mill signal is not automatically E1-S;
- Pilot B inclusion probabilities follow the frozen two-phase design;
- unresolved adjudications are not silently recoded negative;
- scenario outputs remain labelled non-empirical.

---

## Pilot B data governance

See:

- `../process/ADJUDICATION_PROTOCOL.md`
- `../process/PILOT_B_DATA_CONTRACT.md`
- `../data/adjudication_template.csv`

No public unretracted-author fraud-score list is allowed.

---

## Next modules

```text
build_pilot_b_frame.py
latent_prevalence.py
citation_dependence.py
contamination_graph.py
knowledge_ghost_half_life.py
rly_cost.py
innovation_delay.py
sleeping_beauty.py
```

Implementation order follows empirical gates rather than story order.
