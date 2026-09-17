# Code — ARIS4C005

## `build_universe.py`

Queries the OpenAlex Works API and writes annual publication-universe counts plus a provenance JSON.

Default target:

```bash
python build_universe.py \
  --start 2000 \
  --end 2025 \
  --types article,review \
  --corpus core \
  --output ../data/openalex_universe_counts.csv \
  --provenance ../data/openalex_universe_provenance.json
```

Optional environment variables:

```bash
OPENALEX_API_KEY=...
OPENALEX_MAILTO=you@example.org
```

The script constructs a denominator only. It does not estimate research misconduct.

## `scenario_model.py`

Runs transparent Monte Carlo/Fermi scenarios from an external parameter JSON.

```bash
python scenario_model.py \
  ../data/scenario_parameters.example.json \
  --output ../data/scenario_output.example.json
```

Every output is tagged `SCENARIO_NOT_EMPIRICAL_ESTIMATE`.

The example parameter file intentionally demonstrates the vivid units requested during idea development:

- problematic works under a hypothetical paper-level rate;
- Researcher-Life-Years;
- equivalent 5-year PhD blocks;
- equivalent 40-year research-career blocks;
- optional Sleeping Beauty candidate / counterfactual non-awakening quantities.

These outputs are **not** allowed into the scientific evidence ledger unless the parameter ranges are independently calibrated and the resulting analysis is explicitly labelled as modelled/scenario evidence.

## Validation note

The execution environment used during initialization did not have direct DNS access to GitHub/OpenAlex from the local container, so live API execution was not used as evidence. API syntax was checked against the current OpenAlex documentation through web access, and the scenario algorithm was independently reproduced in Python to verify its numerical logic. Production CI should run `python -m py_compile` and unit tests inside GitHub Actions where network-independent tests can execute.

## Planned modules

```text
classify_retractions.py
latent_prevalence.py
contamination_graph.py
citation_dependence.py
innovation_delay.py
sleeping_beauty.py
```

They will be implemented after the denominator/correction pilot fixes the actual data contracts rather than guessing schemas too early.
