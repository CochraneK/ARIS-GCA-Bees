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

## Pilot 1B primary-field multi-outcome benchmark

The next locked frame uses:

- `primary_topic.field.id` rather than any-topic field;
- reproducible OpenAlex `sample + seed`;
- no sampling filter based on current citation count, awards, retractions,
  author fame, or later status;
- multiple future outcome definitions.

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

#### O4 — Awakening within horizon

Binary label:
- retrospective awakening time occurs after cutoff;
- awakening occurs within a prespecified H-year future horizon.

Default H = 15 years.

#### O5 — Delayed-recognition consensus

Binary label requiring at least two of:

- top 20% full-history Beauty Coefficient;
- top 20% immediate future acceleration;
- post-cutoff awakening within H years.

This exists to reduce dependence on any one arbitrary operational definition.

It remains a benchmark definition rather than a claim of importance.

## Citation-only baselines

Pilot 1 must evaluate all of these before any learned model:

1. current citations at cutoff;
2. recent 3-year citation momentum;
3. recent 3-year acceleration;
4. partial-trajectory Beauty Coefficient;
5. dormancy / longest zero-citation run.

A later multi-evidence model is interesting only if it adds value over these.

## Sampling strata

Pilot 1 will expand across:

- multiple publication eras;
- multiple primary fields;
- multiple reproducible seeds.

The first stratum is:

- 1980;
- Physics & Astronomy;
- cutoff 1995;
- endpoint 2011.

Planned additional strata should include at least:

- a life-science/medicine field;
- a social-science field;
- an engineering/computer-science field;
- a later publication era.

## Important temporality caveat

OpenAlex topic/field assignments are current classification metadata and the
topic system itself is produced using modern models/data.

In Pilot 1 these assignments are used only to define/audit strata, not as
prospective predictor features.

Before confirmatory cross-field claims, test whether using current field
classification creates material selection bias. If necessary, replace it with
historically reconstructible source/journal strata or a frozen external
classification.

## Recognition floor sensitivity

Beauty Coefficient can be high for sparse trajectories with very few eventual
citations.

Therefore later Pilot 1 analyses must add sensitivity checks such as:

- minimum total future citation count;
- future field/cohort citation percentile;
- Bcp / under-cited Sleeping Beauty alternatives;
- outcome definitions that combine delayed recognition with later uptake.

Do not silently redefine B itself to solve this.

## Success criteria for Pilot 1

Pilot 1 is complete when:

1. at least several non-hand-picked field/era/seed strata are processed;
2. all five citation baselines are evaluated under all standard outcomes;
3. sample membership and seeds are reproducible;
4. post-cutoff feature leakage tests pass;
5. outcome sensitivity is reported;
6. recognition-floor sensitivity is reported;
7. results are aggregated with uncertainty, not only one tiny cohort;
8. at least one semantic/network feature family is added as an ablation;
9. failure cases are manually inspected.

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
