# ARIS4C015 Pilot 1 — Historical Rediscovery Benchmark

Updated: 2026-09-18

## Purpose

Pilot 1 is the first non-hand-picked historical backtest of ARIS4C015.

It asks:

> At a historical cutoff T, can simple cutoff-safe evidence rank papers that
> later display delayed-recognition outcomes better than naive alternatives?

Pilot 1 does **not** yet test the final multi-evidence agent and does not claim
to predict scientific truth, intrinsic importance, or future breakthroughs.

Its first job is to establish how difficult the benchmark is and how strong
simple citation-only baselines already are.

## Why Pilot 0 is not enough

Pilot 0 established:

- metric fidelity;
- citation-history reconstruction;
- historical leakage controls;
- ARIS4C011 integration semantics;
- cross-database replication on three known Sleeping Beauty cases.

Those known cases are selected examples. They cannot estimate prospective
performance.

Pilot 1 therefore uses reproducible random cohorts rather than famous cases.

## Pilot 1A exploratory smoke — completed

Initial frame:

- OpenAlex;
- publication year 1980;
- article;
- `topics.field.id:31`;
- N = 20;
- seed = 15015;
- cutoff = 1995;
- endpoint = 2011;
- outcome = top 20% full-history Beauty Coefficient in the sampled cohort.

Result:

| Baseline | Precision@5 | Recall@5 | NDCG@5 |
|---|---:|---:|---:|
| current citations | 0.20 | 0.25 | 0.246 |
| 3y momentum | 0.40 | 0.50 | 0.541 |
| 3y acceleration | 0.60 | 0.75 | 0.805 |
| partial B | 0.40 | 0.50 | 0.541 |
| dormancy | 0.00 | 0.00 | 0.000 |

This run proves the non-hand-picked pipeline works.

It is **exploratory only** for two reasons:

1. `topics.field.id:31` means any assigned topic can belong to Physics &
   Astronomy. The resulting sample included a paper whose primary topic was
   Social and Intergroup Psychology.
2. The sole outcome was final Beauty Coefficient top 20%, which is structurally
   related to citation dynamics and may favor citation-acceleration baselines.

Therefore the apparent strength of 3-year acceleration is not treated as a
substantive result.

## Pilot 1B primary-field multi-outcome benchmark — first stratum complete

The locked frame uses:

- `primary_topic.field.id` rather than any-topic field;
- reproducible OpenAlex `sample + seed`;
- no sampling filter based on current citation count, awards, retractions,
  author fame, or later status;
- multiple future outcome definitions;
- later-uptake sensitivity kept separate from delayed-recognition definitions.

The first primary-field stratum is:

- 1980 Physics & Astronomy;
- N = 20;
- seed = 15015;
- cutoff = 1995;
- endpoint = 2011.

This first stratum confirms that baseline ordering changes materially across
outcome definitions, so no single baseline is declared best.

### Standard outcome bundle

#### O1 — Beauty percentile

Graded within-cohort percentile of full-history Beauty Coefficient through the
observation endpoint.

Evaluation:
- NDCG@K.

#### O2 — Beauty top fraction

Binary top 20% full-history B within the cohort.

Evaluation:
- Precision@K;
- Recall@K;
- NDCG@K.

This is a benchmark label, not a universal Sleeping Beauty definition.

#### O3 — Future acceleration percentile

Graded percentile of the change from the recent pre-cutoff citation rate to the
first up-to-three-year post-cutoff citation rate.

Evaluation:
- NDCG@K.

#### O4 — Future uptake percentile

Graded percentile of total citations accumulated in the held-out post-cutoff
window.

This is an attention/uptake outcome, not a delayed-recognition definition on
its own.

#### O5 — Awakening within horizon

Binary label:
- retrospective awakening time occurs after cutoff;
- awakening occurs within a prespecified H-year future horizon.

Default H = 15 years for the 1980 strata and 10 years for 1990 strata whose
endpoint is 2011.

#### O6 — Delayed-recognition consensus

Binary label requiring at least two of:

- top 20% full-history Beauty Coefficient;
- top 20% immediate future acceleration;
- post-cutoff awakening within H years.

This exists to reduce dependence on any one arbitrary operational definition.

It remains a benchmark definition rather than a claim of importance.

#### O7 — Delayed-recognition consensus with uptake floor

A sensitivity label:

1. first satisfy O6 delayed-recognition consensus;
2. also fall within a prespecified higher-uptake share of the cohort during the
   held-out future window.

Current exploratory default:
- top 50% future uptake.

This label exists because B can be high for sparse trajectories that remain
little cited. It must be reported alongside, not substituted for, raw B and O6.

**Do not silently redefine the Beauty Coefficient to add an impact threshold.**

## Citation-only baselines

Pilot 1 must evaluate all of these before any learned model:

1. current citations at cutoff;
2. recent 3-year citation momentum;
3. recent 3-year acceleration;
4. partial-trajectory Beauty Coefficient;
5. dormancy / longest zero-citation run.

A later multi-evidence model is interesting only if it adds value over these.

## Multi-stratum expansion

The first automated multi-stratum batch is locked to five strata:

| Stratum | Year | Primary field | Field ID | Cutoff | Endpoint | Seed |
|---|---:|---|---:|---:|---:|---:|
| Physics 1980 | 1980 | Physics & Astronomy | 31 | 1995 | 2011 | 15015 |
| Medicine 1980 | 1980 | Medicine | 27 | 1995 | 2011 | 27015 |
| Social Sciences 1980 | 1980 | Social Sciences | 33 | 1995 | 2011 | 33015 |
| Physics 1990 | 1990 | Physics & Astronomy | 31 | 2000 | 2011 | 31590 |
| Computer Science 1990 | 1990 | Computer Science | 17 | 2000 | 2011 | 17015 |

Each stratum targets N = 20 and uses the same five citation baselines.

Aggregation is macro across strata rather than naïvely pooling all papers. This
prevents a high-output/high-citation field from dominating the exploratory
summary.

## Important temporality caveat

OpenAlex topic/field assignments are current classification metadata and the
topic system itself is produced using modern models/data.

In Pilot 1 these assignments are used only to define/audit strata, not as
prospective predictor features.

Before confirmatory cross-field claims, test whether using current field
classification creates material selection bias. If necessary, replace it with
historically reconstructible source/journal strata or a frozen external
classification.

## Recognition-floor sensitivity

Beauty Coefficient can be high for sparse trajectories with very few eventual
citations.

Implemented sensitivity outputs now include:

- future-uptake percentile;
- delayed-recognition consensus + top-fraction future-uptake floor.

Future extensions should also compare:

- minimum absolute future citation counts;
- field/cohort-normalized future citation percentiles;
- Bcp / under-cited Sleeping Beauty alternatives.

Recognition floors are outcome sensitivity analyses. They must never leak into
prospective features.

## Success criteria for Pilot 1

Pilot 1 is complete when:

1. at least several non-hand-picked field/era/seed strata are processed;
2. all five citation baselines are evaluated under all seven standard outcomes;
3. sample membership and seeds are reproducible;
4. post-cutoff feature leakage tests pass;
5. outcome sensitivity is reported;
6. recognition-floor sensitivity is reported;
7. results are aggregated with uncertainty, not only one tiny cohort;
8. at least one semantic/network feature family is added as an ablation;
9. failure cases are manually inspected;
10. conclusions survive at least one seed-sensitivity pass.

## Failure / redesign triggers

Redesign before modeling if:

- results are dominated by one arbitrary label definition;
- random-seed changes reverse conclusions;
- source coverage or field classification drives rankings;
- zero/near-zero cited papers dominate delayed-recognition positives;
- simple current citation/momentum baselines explain nearly everything;
- historical feature reconstruction cannot be made cutoff-safe.

## Model-development gate

Do not train a serious prospective model merely because one N=20 cohort gives
high Precision@K.

Prospective modeling begins only after Pilot 1 demonstrates a stable,
non-trivial target across multiple strata and definitions.
