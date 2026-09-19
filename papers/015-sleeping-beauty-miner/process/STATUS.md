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

## Pilot M known-case enrichment · current canonical state

Three literature-reference cases remain the frozen primary Pilot-M cases:

- Hummers & Offeman 1958 — DOI 10.1021/ja01539a017;
- Einstein-Podolsky-Rosen 1935 — DOI 10.1103/PhysRev.47.777;
- Washburn 1921 — DOI 10.1103/PhysRev.17.273.

### Acquisition and design hardening

The earlier v3 50-controls/case run was useful as a smoke test but exposed two
problems during scale-up:

1. OpenAlex `sample=N` does not produce nested samples when N changes, so
   comparing 50 vs 100 directly changed the control pool rather than merely
   enlarging it.
2. the original matcher used global no-replacement across distinct case risk
   sets, which is not the intended incidence-density semantics and introduced
   case-order-dependent depletion.

Current corrections:

- deterministic multi-seed acquisition creates nested unique support pools
  beyond the one-page 100-work limit;
- the same eligible control may be reused across distinct case event-time risk
  sets, while controls remain unique within a single case risk set;
- the primary case set is frozen to the 3 literature-known SBs; robust
  candidates discovered incidentally in the random control reservoir are
  recorded but do not silently become primary cases;
- acquisition and analysis are decoupled: saved cohort artifacts can be
  reanalysed offline without re-querying OpenAlex;
- the prespecified observed-balance gate remains absolute SMD < 0.10 and has
  not been relaxed.

### 603-paper acquisition and frozen-case reanalysis

The deterministic multi-seed acquisition used 200 controls per literature-known
case and produced 603 records including the 3 injected known cases.

Key comparisons:

- v5, 200-control nested reservoir, all robust cases, old global
  no-replacement: max abs SMD = 2.119;
- v6, same reservoir with incidence-density control reuse: max abs SMD = 1.786;
- v7, same reservoir with 4 controls/case and all robust cases: max abs SMD =
  3.112;
- offline frozen-known-case 1:1 reanalysis: 3/3 cases matched, max abs SMD =
  1.633;
- offline frozen-known-case 1:4 reanalysis: 12 matched rows, max abs SMD =
  2.417.

Therefore increasing controls per case does not rescue the balance gate; it
forces weaker controls into sparse historical risk sets.

Canonical diagnostic:
`data/pilotM_riskset_diagnostics_2026-09-19.json`.

### Common-support diagnosis

Within the already acquired cohort, eligible at-risk-dormant controls were
numerous in count but often poor in event-time comparability:

- EPR 1935: 197 eligible controls; minimum sleep-rate gap = 0.438;
- Washburn 1921: 198 eligible controls; minimum sleep-rate gap = 1.180;
- Hummers 1958: 195 eligible controls; minimum sleep-rate gap = 0.063.

Washburn 1921 is the clearest common-support problem. The next scientifically
valid step is therefore to enumerate the complete same-field × same-year frame
before changing the estimand or matching rule. Do not relax the SMD threshold
to force a pass.

Current state:

- mechanism_ready = true;
- mechanism_analysis_ready = false.

Current block reasons:

1. the frozen primary risk-set comparison lacks acceptable observed-covariate
   common support in the acquired reservoir;
2. OpenAlex Beauty-Coefficient / annual-trajectory calibration remains
   provisional;
3. the live OpenAlex acquisition route reached its API rate limit during the
   v8 reacquisition attempt, although offline reanalysis remains operational.

Do **not** run or report a substantive mechanism regression yet.

### Provisional candidates

Two provisional candidates were independently cross-checked for bibliographic
identity and evidence of later scientific use:

- W2018826127 — *An Experimental Study of the Reflection of X-Rays from
  Calcite* — DOI 10.1103/PhysRev.17.608;
- W2006869700 — *Some Studies Concerning Rotating Axes and Polyatomic
  Molecules* — DOI 10.1103/PhysRev.47.552.

Their identity/later-use cross-check passed, but their annual citation
trajectories and OpenAlex Beauty Coefficients are **not** yet independently
validated. They remain provisional and are excluded from the frozen primary
case set.

Canonical note:
`process/PILOTM_PROVISIONAL_CANDIDATE_VALIDATION.md`.

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

1. Enumerate the complete same-field × same-publication-year OpenAlex frame for
   the 3 frozen literature-known cases; do not draw another random reservoir.
2. Keep abs SMD < 0.10 fixed; do not rescue the design by post-hoc relaxation.
3. Re-run the frozen 1:1 event-time support diagnostic on the complete frame.
4. If complete-frame overlap still fails, freeze an overlap-limited estimand or
   unmatched-case rule before any mechanism inference.
5. Independently validate OpenAlex annual citation trajectories / Beauty
   Coefficient against SciSciNet-v2 or another bibliographic source.
6. Expand the confirmed-SB cohort only after cross-source validation.
7. Only after acceptable balance, add mechanism families:
   - reference combinations;
   - network/core-periphery position;
   - field readiness / semantic neighborhood;
   - Prince / awakening path;
   - optional patent / technology transfer.
8. Connect real ARIS4C011 findings for the same cases.
9. Continue Track B independently with chronological and field/era holdouts.
10. Train learned prospective models only after independent feature families
   show stable value over transparent baselines.

## Current blockers / constraints

- primary risk-set common support / observed balance still fails, especially
  for the Washburn 1921 stratum;
- OpenAlex B calibration is provisional;
- SciSciNet-v2 execution awaits an available BigQuery/GCS route;
- modern field/topic classifications may back-project imperfectly onto old
  papers;
- bibliographic-source coverage affects B and awakening geometry;
- prospective predictive validity remains unestablished.

## CI / reproducibility checkpoint

Latest design-code checkpoints:
- frozen primary-case selection CI: run 35436038223 — success;
- offline frozen-case reanalysis: run 35436185652 — success;
- offline common-support diagnostics: run 35436185652 successor workflow path,
  with the diagnostic JSON checkpointed in Git.

The live v8 reacquisition attempt failed only because OpenAlex returned HTTP
429 with the current rate window exhausted; the acquired v7 cohort remains
usable offline.

## Recovery

For a new chat / agent / computer:

1. read process/HANDOFF.md;
2. read this STATUS.md;
3. inspect latest ARIS4C015 GitHub Actions;
4. continue the Immediate next gates above.

The original ChatGPT thread is not required for scientific continuity.
