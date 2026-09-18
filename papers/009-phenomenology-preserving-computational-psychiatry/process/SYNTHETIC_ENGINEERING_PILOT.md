# ARIS4C009A · Synthetic engineering pilot

**Status:** synthetic only — not empirical evidence.

## Purpose

Before collecting any psychiatric data, test whether the proposed analysis machinery can represent the expected trade-off structure.

The synthetic generator in:

`code/simulate_fidelity_benchmark.py`

creates hypothetical query-level reconstruction outcomes for six representation types over five domains.

The input probabilities are illustrative assumptions chosen to exercise the pipeline. They are **not** estimates from patients or literature.

## Frozen engineering run

Parameters:

- random seed: 20260918;
- episodes: 300;
- queries per domain per episode: 8;
- domains: concrete, agency, minimal self, context, temporal.

Reproduced output from the frozen synthetic run:

| Representation | Concrete | Agency | Minimal self | Context | Temporal | Overall | Burden min |
|---|---:|---:|---:|---:|---:|---:|---:|
| R0 rich source | 0.960 | 0.946 | 0.915 | 0.960 | 0.940 | 0.944 | 120 |
| R1 episode graph | 0.924 | 0.887 | 0.882 | 0.914 | 0.908 | 0.903 | 45 |
| R2 expert phenomenology | 0.889 | 0.916 | 0.902 | 0.849 | 0.863 | 0.884 | 60 |
| R3 self-report | 0.810 | 0.683 | 0.614 | 0.650 | 0.667 | 0.685 | 8 |
| R4 symptom scale | 0.853 | 0.620 | 0.476 | 0.489 | 0.585 | 0.604 | 15 |
| R5 low-dimensional | 0.732 | 0.590 | 0.463 | 0.451 | 0.525 | 0.552 | 3 |

The two-axis engineering Pareto frontier under **overall synthetic fidelity versus burden only** retains:

- R0 rich source;
- R1 episode graph;
- R3 self-report;
- R5 low-dimensional.

R2 and R4 become dominated under these arbitrary assumptions.

## Why this pilot is useful

The result is not interesting substantively. The engineering properties are:

1. the pipeline can represent domain-specific fidelity rather than a single score;
2. a richer representation does not automatically become the universal winner once burden is included;
3. a Pareto analysis can identify dominated representations without imposing a subjective weighted total;
4. the same machinery can later accept empirical estimates and uncertainty intervals.

## What this pilot does **not** establish

It does not show that:

- interviews really achieve 0.94 fidelity;
- self-report really loses this much information;
- an episode graph is superior to specialist phenomenology;
- these burdens are realistic;
- psychosis is uniquely susceptible to compression loss.

All numerical assumptions must be replaced by observed data.

## Next engineering tests

Before confirmatory data:

- add hierarchical episode/evaluator random effects;
- simulate source ambiguity and abstention;
- simulate unequal representation lengths;
- test rate-matched comparisons;
- propagate uncertainty into Pareto membership;
- run power/precision simulations over plausible effect sizes rather than one assumed scenario.
