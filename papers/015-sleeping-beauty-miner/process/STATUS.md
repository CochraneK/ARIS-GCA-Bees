# ARIS4C015 Status

Updated: 2026-09-18

## Stage

**Pilot 1 historical benchmark + Mechanism Track implementation.**

ARIS4C015 now has three separate research tracks:

- Track A: retrospective robust Sleeping Beauty identification;
- Track M: case-enriched mechanism discovery with matched controls;
- Track B: random/time-safe prospective rediscovery benchmark.

A validated prospective Sleeping Beauty prediction model does not yet exist.

## Pilot M multi-stratum yield diagnostic

A bounded real-data mechanism-yield benchmark was run across five reproducible OpenAlex strata (Physics 1980, Medicine 1980, Social Sciences 1980, Physics 1990, Computer Science 1990), 100 papers per stratum.

Result:
- papers analyzed: **500**;
- robust Sleeping Beauties under the current strict gate: **0**;
- mechanism-ready strata: **0/5**;
- mechanism-analysis-ready strata: **0/5**;
- selection on future citation count: **false**.

Interpretation: this is a scientifically useful negative yield result, not evidence that Sleeping Beauties do not exist. It demonstrates that small random historical cohorts cannot be assumed to contain robust SB cases and therefore cannot support mechanism analysis. Track M must now receive cases from a larger retrospective Track-A discovery corpus rather than forcing positives in random samples.

Workflow: `ARIS4C015 Pilot M Multi-Stratum` run `35406774616`.

## Track A retrospective discovery · successful throttled run

The public-API-safe serial Track-A workflow completed across three outcome-enriched strata:

- Physics 1980: 50 screened, **4 robust SB**, 16 near-gate;
- Medicine 1980: 50 screened, **3 robust SB**, 5 near-gate;
- Computer Science 1990: 50 screened, **6 robust SB**, 11 near-gate;
- total: **150 screened, 13 unique strict robust SB**.

This cohort is deliberately enriched using present-day citation count to reduce retrospective case-discovery cost. Therefore:
- **prevalence estimation is forbidden** from this sample;
- **prospective predictive-performance claims are forbidden** from this sample.

This result complements the unselected 500-paper mechanism-yield diagnostic (0 robust SB): random small cohorts are suitable for prospective benchmarking, whereas Track A requires retrospective enrichment to efficiently find mechanism cases.

Successful workflow run: `35407583375`.

## Track M matched-control gate · first empirical pass

A same-field/year matched-control mechanism pilot was completed using:
- retrospectively outcome-enriched strict SB cases;
- independently sampled **unselected** control pools;
- exact field/year matching;
- prespecified early-attention caliper = 0.15;
- no control replacement.

Result across three strata:
- robust SB cases: **13**;
- Forgotten controls available: **67**;
- matched SB cases: **1/13**;
- analysis-ready strata: **0/3**.

By stratum:
- Computer Science 1990: 6 SB, 23 Forgotten, 0 matched;
- Medicine 1980: 3 SB, 22 Forgotten, 0 matched;
- Physics 1980: 4 SB, 22 Forgotten, 1 matched (25%).

Interpretation: the current **50-paper unselected control reservoir per stratum is insufficient under the frozen matching rule**. This is a matching-support failure, not evidence against an SB mechanism. The next step is to enlarge the unselected control reservoir while holding the caliper and matching variables fixed; the gate must not be rescued by outcome-driven relaxation.

Workflow run: `35412163832`.

## Completed

### Core agent / engineering

- reusable sleeping-beauty-miner Skill;
- deterministic orchestrator and Candidate Evidence Card;
- complete yearly citation-history reconstruction;
- Beauty Coefficient and awakening time;
- OpenAlex and local SciSciNet-style cutoff-safe adapters;
- OpenAlex retry/backoff and request-volume hardening;
- ARIS4C011 integrity routing;
- transparent citation baselines;
- ranking / calibration metrics;
- local discovery scan;
- CI and live empirical workflows.

### Pilot 0 cross-source metric validation

Three classic delayed-recognition cases were reconstructed from OpenAlex through
the 2011 observation endpoint and compared with Ke et al. / WoS values.

Result:
- exact awakening-year match in 2/3 cases;
- all within 3 years;
- mean absolute awakening-year difference: 1 year;
- B values differed by about 13.3% on average.

Interpretation:
- awakening geometry appears more cross-source stable than absolute B in this
  tiny selected probe;
- this is implementation validation, not general evidence.

### Pilot 1 citation-baseline benchmark

Current benchmark:
- 5 field/era groups;
- 2 fixed random seeds each;
- 10 strata;
- 20 papers per stratum;
- 200 target papers total;
- 7 future outcome definitions;
- 5 transparent citation baselines.

Key result:
- partial B strongly predicts future B-defined outcomes;
- current citations / momentum strongly predict future citation uptake;
- no citation-only baseline consistently dominates awakening or
  delayed-recognition-consensus outcomes.

For delayed-recognition consensus, macro NDCG@5 across 10 strata was roughly:
- partial B: 0.357;
- acceleration: 0.341;
- current citations: 0.216;
- momentum: 0.214;
- dormancy: 0.204.

Cross-stratum variance remains large.

### Recognition-floor sensitivity

A top-50% future-uptake floor was too weak to change the consensus label.

A stricter top-25% uptake sensitivity reduced positive cases in several strata,
showing that delayed geometry and substantial later recognition should remain
distinct outcome dimensions.

### First non-citation ablation

Historical title lexical novelty was evaluated across the same 10 strata.

Signals:
- nearest-1 prior-title distance;
- nearest-3 prior-title distance;
- OOV token share.

Result:
- no stable improvement over the strongest citation-only baseline for
  delayed-recognition consensus;
- nearest-3 distance roughly tied citation acceleration on awakening in this
  exploratory sample;
- target vocabulary coverage from the 100-title prior corpus was limited.

Current interpretation:
- simple small-corpus lexical novelty is a negative / insufficient ablation;
- this does not establish that semantic novelty in general is uninformative.

## Mechanism Track correction

A random prospective cohort may contain zero genuine Sleeping Beauties.

Therefore cohort-relative top-q outcomes are no longer allowed to function as
mechanism labels.

Implemented mechanism infrastructure:

- literature-style sleep/depth/wake gate;
- source-calibrated B gate;
- later-recognition floor;
- robust-SB convergence rule;
- field x publication-year early/late normalization;
- canonical trajectory states:
  - SLEEPING_BEAUTY;
  - FORGOTTEN;
  - IMMEDIATE_HIT;
  - FADING;
  - AMBIGUOUS;
  - LOW_EARLY_HIGH_LATE_UNCONFIRMED;
- deterministic matched controls;
- primary contrasts:
  - SB vs Forgotten;
  - SB vs Immediate Hit;
- mechanism_ready hard gate.

If zero robust SBs pass:
- mechanism_ready=false;
- mechanism claims are blocked;
- relative top-q benchmark positives cannot be renamed as SBs.

See process/MECHANISM_TRACK.md.

## Data strategy for true mechanism cases

Preferred large-scale route:

1. use SciSciNet / SciSciNet-v2 precomputed SB_B as a cheap candidate prefilter;
2. require sufficient later citation uptake;
3. reconstruct complete annual trajectories for candidates;
4. apply the robust SB gate;
5. construct field/cohort-matched Forgotten / Immediate-Hit controls;
6. analyze semantic/network/Prince/technology mechanisms.

SciSciNet v1 reports:
- B > 33 as approximately its top 2% SB group;
- B > 307.55 as its top-10,000 high-B group.

These thresholds are source-specific calibration references and must not be
treated as universal constants.

## Immediate next gates

1. Freeze the 13 current robust Track-A cases with provenance and threshold sensitivity.
2. Build an **unselected** same-field/year control reservoir with the same 2025 endpoint.
3. Quantify match yield and balance for SB vs Forgotten and SB vs Immediate Hit.
4. Expand retrospective discovery beyond the current 150 enriched candidates only after the matching gate is characterized.
5. Add reference-combination / citation-network mechanism features.
6. Run Prince / awakening-path analysis on confirmed cases.
7. Expand prospective Pilot 1 beyond citation baselines and simple lexical
   novelty.
8. Connect real ARIS4C011 findings to the same papers.
9. Only then consider learned prospective ranking models.

## Current blockers / constraints

- no canonical SciSciNet-v2 query/slice is yet attached to the project;
- Mechanism Track is implemented but not yet populated with a large empirical
  robust-SB cohort;
- current field/topic assignments may use modern classifications;
- bibliographic-source coverage affects B;
- prospective predictive validity remains unknown.

## Promotion gates

### Mechanism Track ready for substantive analysis when

- a large retrospective corpus yields a non-trivial number of robust SBs;
- threshold sensitivity is reported;
- matched-control yield is acceptable;
- covariate balance is audited;
- mechanism features are computed without contaminating matching variables.

### Prospective model-development gate

Do not train a serious model until:
- multiple delayed-recognition outcomes remain non-trivial across strata;
- independent feature families are tested;
- simple baselines are not sufficient;
- chronological and field/era holdouts are specified;
- no known post-cutoff leakage remains.

### Prospective validation gate

Requires:
- chronological train/validation/test;
- leave-field / leave-era evaluation;
- calibrated probabilities if emitted;
- human-review utility;
- shortcut/prestige audits;
- independent replication where feasible.
