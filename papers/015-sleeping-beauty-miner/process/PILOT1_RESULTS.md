# ARIS4C015 Pilot 1 Results — Citation Baseline Stage

Updated: 2026-09-18

## Status

**Citation-baseline stage complete for the first two-seed multi-stratum benchmark.**

Current evidence base:

- 5 field/era groups;
- 2 fixed random seeds per group;
- 10 independent strata;
- 20 papers per stratum;
- 200 target papers total;
- 7 future outcome definitions;
- 5 transparent citation baselines.

One stratum initially encountered an OpenAlex HTTP 429. It was repaired after
adding bounded exponential backoff and removing redundant target metadata
requests. The scientific result was not imputed.

This is still exploratory Pilot 1, not prospective-model validation.

## Sampling design

| Group | Cohort | Cutoff | Endpoint | Seeds |
|---|---:|---:|---:|---|
| Physics & Astronomy | 1980 | 1995 | 2011 | 15015, 15016 |
| Medicine | 1980 | 1995 | 2011 | 27015, 27016 |
| Social Sciences | 1980 | 1995 | 2011 | 33015, 33016 |
| Physics & Astronomy | 1990 | 2000 | 2011 | 31590, 31591 |
| Computer Science | 1990 | 2000 | 2011 | 17015, 17016 |

Within each field/era group, the two 20-paper samples had Jaccard overlap 0 in
this run. Therefore the second seed is a materially different sample rather
than a near-duplicate.

OpenAlex primary-field assignments are current metadata and are used only to
define exploratory strata, not as predictor values.

## Outcome prevalence is not constant

Delayed-recognition consensus positive rates differed across seeds and strata:

| Group | Seed 1 | Seed 2 |
|---|---:|---:|
| Physics 1980 | 20% | 20% |
| Medicine 1980 | 15% | 20% |
| Social Sciences 1980 | 5% | 15% |
| Physics 1990 | 5% | 15% |
| Computer Science 1990 | 20% | 20% |

This is one reason not to use a single unstratified global threshold without
further calibration.

## Macro NDCG@5 across 10 strata

### Beauty percentile

| Baseline | Mean | SD |
|---|---:|---:|
| current citations | 0.633 | 0.159 |
| 3y momentum | 0.659 | 0.138 |
| 3y acceleration | 0.694 | 0.120 |
| partial B | **0.888** | 0.062 |
| dormancy | 0.413 | 0.105 |

Interpretation:

Partial B performs strongly because the future outcome is itself defined by the
same delayed-recognition geometry. This is a useful benchmark but not
independent evidence that prospective rediscovery has been solved.

### Beauty top fraction

| Baseline | Mean | SD |
|---|---:|---:|
| current citations | 0.289 | 0.212 |
| 3y momentum | 0.358 | 0.229 |
| 3y acceleration | 0.457 | 0.225 |
| partial B | **0.644** | 0.229 |
| dormancy | 0.162 | 0.149 |

Again, definition alignment is substantial.

### Immediate future acceleration percentile

| Baseline | Mean | SD |
|---|---:|---:|
| current citations | 0.493 | 0.199 |
| 3y momentum | 0.427 | 0.227 |
| 3y acceleration | 0.513 | 0.157 |
| partial B | 0.597 | 0.209 |
| dormancy | **0.662** | 0.142 |

Dormancy performs best on average here, but the purpose of this outcome is
short-horizon change rather than a complete Sleeping Beauty definition.

### Future uptake percentile

| Baseline | Mean | SD |
|---|---:|---:|
| current citations | **0.883** | 0.071 |
| 3y momentum | 0.846 | 0.090 |
| 3y acceleration | 0.699 | 0.112 |
| partial B | 0.723 | 0.111 |
| dormancy | 0.391 | 0.083 |

This is expected persistence: already-cited papers tend to accumulate more
future citations. It is not delayed-recognition prediction.

### Awakening within horizon

| Baseline | Mean | SD |
|---|---:|---:|
| current citations | 0.152 | 0.224 |
| 3y momentum | 0.167 | 0.229 |
| 3y acceleration | **0.291** | 0.231 |
| partial B | 0.257 | 0.201 |
| dormancy | 0.209 | 0.203 |

No baseline is stable here. Winner counts are distributed across acceleration,
partial B, dormancy, current citations, and momentum.

### Delayed-recognition consensus

| Baseline | Mean | SD |
|---|---:|---:|
| current citations | 0.216 | 0.250 |
| 3y momentum | 0.214 | 0.267 |
| 3y acceleration | 0.341 | 0.208 |
| partial B | **0.357** | 0.227 |
| dormancy | 0.204 | 0.191 |

The difference between partial B and acceleration is small relative to
cross-stratum variation. NDCG winner counts are split:

- partial B: 3 strata;
- acceleration: 3;
- dormancy: 3;
- momentum: 2.

Counts exceed 10 because exact ties count for each tied strategy.

**There is currently no citation-only winner that can reasonably be called a
stable rediscovery predictor.**

## Recognition-floor sensitivity

The original top-50% future-uptake floor did not change consensus labels in the
first 10 strata.

A stricter offline sensitivity analysis required:

> delayed-recognition consensus AND top 25% held-out future uptake.

This reduced positive counts substantially in several cohorts, especially
Medicine and Physics.

Macro NDCG@5 under the stricter label:

| Baseline | Mean NDCG@5 |
|---|---:|
| current citations | 0.242 |
| 3y momentum | 0.243 |
| 3y acceleration | 0.327 |
| partial B | **0.428** |
| dormancy | 0.097 |

This shows that a recognition floor is scientifically consequential rather than
a cosmetic reporting choice.

It remains a sensitivity definition and is never used as a prospective
feature.

## What has been learned

### 1. Benchmark plumbing works on non-hand-picked data

The project has moved beyond classic-example replication. Historical cutoff
reconstruction, multiple outcomes, fixed review budgets, and cross-stratum
aggregation now work on random OpenAlex cohorts.

### 2. Outcome definition matters greatly

A method can look strong when the future outcome shares the same mathematical
structure:

- partial B -> future B;
- current citations / momentum -> future citation uptake.

Those results are expected baselines, not the main scientific contribution.

### 3. The actual rediscovery target remains difficult

Awakening and multi-definition consensus are substantially less stable than
future citation count or future B.

That instability is scientifically useful: it creates a non-trivial benchmark
for independent evidence families.

### 4. Seed sensitivity is material

Consensus prevalence and baseline rankings can change under a second disjoint
sample from the same field/era.

Therefore no single N=20 cohort is sufficient evidence.

### 5. Citation-only prediction is not enough

No citation-only baseline consistently dominates delayed-recognition consensus
across field/era/seed strata.

The next question is whether evidence available at publication/cutoff that is
not simply citation momentum adds reproducible information.

## Next ablation

The first independent feature family is intentionally simple and auditable:

**historical title lexical novelty**

Signals:

- nearest-1 prior-title TF-IDF distance;
- nearest-3 mean prior-title distance;
- OOV-token share against a pre-target title corpus.

For each field/era pair:

- target outcomes remain frozen;
- the two target seeds share the same pre-target reference corpus;
- prior titles strictly precede the target publication year;
- no future citations enter feature construction;
- no modern embedding is used.

If this feature family fails, it will be retained as a negative ablation result
rather than being promoted into the final agent.

## Remaining limitations

- N=20 per stratum is still small.
- Only five field/era groups are represented.
- OpenAlex field assignments are current classifications.
- Citation coverage is source-dependent.
- The current benchmark outcome ontology is not yet externally validated.
- No validated learned prospective model exists.
- Semantic/network/technology/integrity feature-family ablations are not yet
  complete.

## Claim boundary

The current result supports the feasibility of a time-safe historical
rediscovery benchmark.

It does **not** establish that ARIS4C015 predicts future breakthroughs or
scientific importance.
