# ARIS4C015 Status

Updated: 2026-09-19

## Stage

**Pilot 1 historical benchmark + Mechanism Track risk-set validation.**

ARIS4C015 has three distinct tracks:

- Track A — retrospective robust Sleeping Beauty identification;
- Track M — case-enriched mechanism discovery;
- Track B — random, historical-cutoff-safe prospective rediscovery.

A validated prospective Sleeping Beauty prediction model does not yet exist.
A substantive mechanism model is also not yet analysis-ready.

Canonical recovery note: process/HANDOFF.md

## Current scientific definition

The current mechanism definition supersedes older percentile-gated notes.

### Robust SB identity

A retrospective mechanism case is defined from the complete citation
trajectory by converging components:

1. variable sleep/depth + awakening-intensity gate;
2. Beauty Coefficient gate;
3. later-recognition floor.

OpenAlex B thresholds are currently provisional references borrowed from
SciSciNet-v1 calibration and are not yet source-validated for OpenAlex.

### Relative trajectory quadrant

Field x publication-year early/late percentiles are retained as a separate
descriptive variable.

They do **not** determine whether a robust case is an SB.

This separation became necessary because classic literature cases such as EPR
and Washburn can rank high in early citation percentile in sparse historical
cohorts while still showing decades-long low-rate sleep.

### Post-awakening fate

A third, separate descriptor records what happens after awakening:

- TRANSIENT_OR_FADED;
- ROUGHLY_SUSTAINED;
- EXPANDED_AFTER_AWAKENING.

It is not part of SB identity.

## Pilot M random-yield diagnostics

### 100-paper OpenAlex smoke

1980 Physics random sample:
- n = 100;
- robust SB = 0;
- mechanism_ready = false.

### 497-paper merged random cohort

Five deterministic 100-paper shards were merged before normalization:
- requested rows = 500;
- unique papers = 497;
- duplicate rows removed = 3;
- robust SB = 0;
- Forgotten = 207;
- Immediate Hit = 85;
- low-early/high-late unconfirmed = 22.

Only one of the 22 unconfirmed papers was a near-miss that passed sleep/wake
and provisional B but had only 29 citations through 2011, below the
prespecified recognition floor of 50.

Decision:
**do not scale random mechanism cohorts merely to wait for rare SB events.**
Random cohorts belong primarily to Track B. Track M should be case-enriched.

Canonical result:
data/pilotM_openalex_500_summary.json

## Pilot M known-case enrichment v3

Three literature-reference cases were injected as known delayed-recognition
cases and surrounded with same-year/same-OpenAlex-field controls:

- Hummers & Offeman 1958 — DOI 10.1021/ja01539a017;
- Einstein-Podolsky-Rosen 1935 — DOI 10.1103/PhysRev.47.777;
- Washburn 1921 — DOI 10.1103/PhysRev.17.273.

Workflow:
- ARIS4C015 Pilot M known-SB case enrichment v3;
- run 35427591815;
- head SHA 3ce9f09975f2858fd362ac4cfe727b815df047c3;
- conclusion: success.

Result:
- papers = 153;
- robust SB = 5;
- all 3 literature-reference cases pass the robust SB gate;
- 2 additional provisional OpenAlex robust-SB candidates were found.

Additional provisional candidates:
- W2018826127 — *An Experimental Study of the Reflection of X-Rays from
  Calcite* — DOI 10.1103/PhysRev.17.608;
- W2006869700 — *Some Studies Concerning Rotating Axes and Polyatomic
  Molecules* — DOI 10.1103/PhysRev.47.552.

These two remain discovery candidates until cross-source validation and
source-specific B calibration.

Canonical result:
data/pilotM_known_cases_v3_summary.json

## Primary mechanism contrast

The primary comparison is now **event-time risk-set matching**:

> At the case SB's awakening time, compare it with a paper from the same field
> and publication year that is still dormant at that event time.

Rules:
- exact field and publication year;
- matching information measured no later than the case event time;
- control must still satisfy the sleep regime at that time;
- control must not already have a qualifying awakening burst;
- a control may awaken later;
- post-event control outcomes are not used to select the match.

Forgotten and Immediate-Hit comparisons remain secondary/extreme contrasts.

### Pilot M v3 risk-set result

Primary SB-vs-at-risk-dormant contrast:
- 5/5 robust SB cases matched;
- match rate = 1.0;
- balance threshold = abs SMD < 0.10;
- sleep-rate-to-event abs SMD ~= 0.950;
- reference-count abs SMD ~= 0.562;
- author-count abs SMD ~= 0.566;
- balance_pass = false.

For comparison, the older SB-vs-Forgotten sleep-rate SMD was ~= 3.317.

Interpretation:
- event-time risk-set matching is directionally better than permanent-Forgotten
  matching;
- the current 50-control-per-known-case reservoir is still too small / too
  weakly supported for acceptable observed-covariate balance;
- match yield alone is not evidence of a valid mechanism comparison.

Current state:
- mechanism_ready = true;
- mechanism_analysis_ready = false.

Current block reasons:
1. SB-vs-at-risk-dormant observed covariates remain imbalanced;
2. Beauty Coefficient threshold is not validated for OpenAlex.

Do **not** run or report a substantive mechanism regression yet.

## Temporal mechanism evidence

Mechanism evidence is partitioned by time:

- M0 — publication-state evidence;
- M1 — sleep-period evidence;
- M2 — awakening-window evidence;
- M3 — post-awakening evidence.

Anti-time-reversal rule:
a later Prince/event can help explain awakening, but cannot be used as evidence
for why the paper was initially neglected without a separate longitudinal or
causal design.

See:
agent/sleeping-beauty-miner/references/SIGNAL_CONTRACT.md

## Track A retrospective discovery

Earlier outcome-enriched Track-A runs found multiple strict robust-gate
candidates, including a 150-paper / 13-candidate run.

Important correction:
older notes that required robust gate **plus** early-low/late-high percentile
for SB identity are superseded by the current identity/quadrant separation.

Track-A enriched samples:
- may efficiently acquire cases;
- may not estimate SB prevalence;
- may not support prospective predictive-performance claims.

## Pilot 0 cross-source validation

Three classic delayed-recognition cases were reconstructed from OpenAlex
through the 2011 endpoint and compared with Ke et al. / WoS reference values.

Observed:
- exact awakening-year match in 2/3 cases;
- all within 3 years;
- mean absolute awakening-year difference = 1 year;
- B differed by about 13.3% on average.

Interpretation:
awakening timing may be more cross-source stable than absolute B in this tiny
selected probe. This is implementation evidence, not a general source-robustness
claim.

## Track B prospective Pilot 1

Current benchmark:
- 5 field/era groups;
- 2 fixed seeds each;
- 10 strata;
- 20 papers per stratum;
- 200 target papers;
- 7 future outcome definitions;
- 5 transparent citation baselines.

Delayed-recognition-consensus macro NDCG@5 was approximately:
- partial B: 0.357;
- acceleration: 0.341;
- current citations: 0.216;
- momentum: 0.214;
- dormancy: 0.204.

Interpretation:
- partial B is strong for future B-defined outcomes;
- current citations / momentum are strong for future citation uptake;
- no citation-only baseline consistently dominates the harder awakening /
  delayed-recognition-consensus outcomes;
- cross-stratum variance remains large.

### Recognition-floor sensitivity

A top-50% future-uptake floor was weak.
A stricter top-25% sensitivity reduced positives in several strata.

Delayed geometry and substantial later recognition therefore remain separate
outcome dimensions.

### First non-citation ablation

Historical title lexical novelty:
- nearest-1 prior-title distance;
- nearest-3 prior-title distance;
- OOV token share.

Result:
no stable improvement over the strongest citation-only baseline for the
delayed-recognition consensus outcome.

This is a negative / insufficient result for this small lexical baseline, not
evidence that semantic novelty in general is uninformative.

## Core implementation completed

- reusable sleeping-beauty-miner Agent Skill;
- Candidate Evidence Card;
- complete annual citation-history reconstruction;
- Beauty Coefficient and awakening time;
- OpenAlex adapter with retry/backoff and reproducible sampling;
- cutoff-safe local SciSciNet-style adapter;
- transparent citation baselines;
- historical backtest and ranking/calibration metrics;
- semantic/network proxy contract;
- Prince candidate extraction;
- ARIS4C011 integrity routing;
- robust SB gate;
- identity/quadrant separation;
- post-awakening fate;
- deterministic secondary matching;
- event-time risk-set matching;
- hard mechanism_ready and mechanism_analysis_ready gates;
- CI and live empirical workflows.

## SciSciNet-v2 route

Preferred large-corpus Track-A / Track-M route:

1. schema discovery;
2. cheap B-based candidate prefilter;
3. complete annual trajectory reconstruction;
4. robust gate;
5. source-specific B calibration / sensitivity;
6. event-time risk-set controls;
7. mechanism features.

Executable SQL templates:
- sql/sciscinet_v2_schema_discovery.sql;
- sql/sciscinet_v2_sb_candidate_counts.sql;
- sql/sciscinet_v2_sb_prefilter.sql.

On 2026-09-19 the ChatGPT BigQuery plugin was present but disabled by admin.
That is an execution-environment constraint, not a scientific blocker.

## Immediate next gates

1. Expand the at-risk control reservoir for confirmed SB cases.
   - first try 100 controls/case;
   - then deterministic multi-seed 200–300 control pools if needed.
2. Keep abs SMD < 0.10 fixed; do not rescue the design by post-hoc relaxation.
3. Cross-validate the two additional provisional OpenAlex SB candidates.
4. Execute SciSciNet-v2 schema discovery and source-specific B calibration when
   BigQuery/GCS access is available.
5. Re-run event-time matching on a larger confirmed SB cohort.
6. Only after acceptable balance, add mechanism families:
   - reference combinations;
   - network/core-periphery position;
   - field readiness / semantic neighborhood;
   - Prince / awakening path;
   - optional patent / technology transfer.
7. Connect real ARIS4C011 findings for the same cases.
8. Continue Track B independently with chronological and field/era holdouts.
9. Train learned prospective models only after independent feature families
   show stable value over transparent baselines.

## Current blockers / constraints

- primary risk-set balance still fails;
- OpenAlex B calibration is provisional;
- SciSciNet-v2 execution awaits an available BigQuery/GCS route;
- modern field/topic classifications may back-project imperfectly onto old
  papers;
- bibliographic-source coverage affects B and awakening geometry;
- prospective predictive validity remains unestablished.

## CI / reproducibility checkpoint

Latest checked code CI after identity / fate / risk-set work:
- workflow: ARIS4C015 Sleeping Beauty Miner CI;
- run: 35427583429;
- head SHA: 8589012e4bc59f9f0d2eef8d9f2f47647026f0d4;
- conclusion: success.

Pilot M v3 also completed successfully.

## Recovery

For a new chat / agent / computer:

1. read process/HANDOFF.md;
2. read this STATUS.md;
3. inspect latest ARIS4C015 GitHub Actions;
4. continue the Immediate next gates above.

The original ChatGPT thread is not required for scientific continuity.
