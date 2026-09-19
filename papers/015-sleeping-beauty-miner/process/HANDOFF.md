# ARIS4C015 Handoff

Updated: 2026-09-19

This file is the canonical recovery note for another ChatGPT thread, account,
computer, coding agent, or human collaborator. Read this before continuing
ARIS4C015. The original chat is not required once this file and STATUS.md are
current.

## Project identity

Repository: CochraneK/ARIS4C
Project path: papers/015-sleeping-beauty-miner/
Working title: Sleeping Beauty Miner: An Integrity-Aware, Time-Safe Agent for
Discovering Delayed and Under-Recognized Scientific Work.

Dependency:
- ARIS4C011 Research Forensics supplies integrity/provenance routing.
- ARIS4C005 may consume buried/under-recognized candidates downstream, but
  causal opportunity-cost claims remain separate.

## Read order

1. process/STATUS.md
2. process/MECHANISM_TRACK.md
3. process/RESEARCH_PLAN.md
4. agent/sleeping-beauty-miner/SKILL.md
5. agent/sleeping-beauty-miner/references/SIGNAL_CONTRACT.md
6. data/pilotM_riskset_diagnostics_2026-09-19.json
7. process/PILOTM_PROVISIONAL_CANDIDATE_VALIDATION.md
8. process/CONVERSATION_LOG.md

## Three tracks

Track A — retrospective identification:
Find robust delayed-recognition papers from complete citation trajectories.
Outcome-enriched retrospective sampling is allowed for efficient case
acquisition, but such samples cannot estimate prevalence or prospective
prediction performance.

Track M — mechanism discovery:
Use robust retrospective SB cases and compare them with controls. The current
primary contrast is event-time risk-set matching:

At the time one SB awakens, compare it with same-field and same-publication-year
papers that are still dormant at that event time.

A control may awaken later. Post-event information is not used to choose the
match. The same eligible paper may be reused across distinct case risk sets,
which is standard incidence-density/risk-set sampling semantics; controls are
not duplicated within one case risk set.

Secondary contrasts:
- SB vs Forgotten;
- SB vs Immediate Hit.

Track B — prospective rediscovery:
Historical-cutoff ranking with no future leakage. Random cohorts belong here.
This is the eventual discovery/mining target.

## Critical invariants

1. Citation attention is not scientific truth or merit.
2. A random cohort is not guaranteed to contain a genuine SB.
3. Relative top-q benchmark labels must never be renamed as mechanism SB cases.
4. Robust SB identity, relative early/late quadrant, and post-awakening fate
   are separate variables.
5. Robust SB identity comes from the complete retrospective trajectory:
   variable sleep/depth + awakening intensity + source-calibrated B +
   later-recognition floor.
6. Relative cohort quadrants are descriptive and cannot veto robust SB identity.
7. Missing evidence is not zero; use ABSTAIN where appropriate.
8. OpenAlex B thresholds used in mechanism smoke tests are provisional,
   borrowed from SciSciNet-v1 references. They cannot support a confirmatory
   mechanism claim until source-specific calibration or cross-source
   validation is complete.
9. mechanism_analysis_ready=false blocks substantive mechanism claims.
10. Integrity findings from ARIS4C011 route review/quarantine; absence of a flag
    is not a positive scientific-quality score.

## Real empirical state

### Random mechanism yield

- 100-paper OpenAlex 1980 Physics smoke: 0 robust SB.
- Five-shard merged 1980 Physics cohort: 497 unique papers, 0 robust SB.
- 22/497 were low-early/high-late unconfirmed.
- Only one was a near-miss that passed sleep/wake + provisional B but had 29
  total citations through 2011, below the recognition floor of 50.

Decision:
Do not keep scaling random mechanism cohorts simply to wait for rare SB events.
Random cohorts remain useful for Track B.

### Known-case enriched real mechanism pilot

Frozen literature-known primary cases:
- Hummers & Offeman 1958, DOI 10.1021/ja01539a017
- Einstein-Podolsky-Rosen 1935, DOI 10.1103/PhysRev.47.777
- Washburn 1921, DOI 10.1103/PhysRev.17.273

The v3 smoke test used 50 controls/case. Subsequent runs corrected two design
issues: OpenAlex sample-size changes were non-nested, and global no-replacement
across risk sets was inconsistent with incidence-density sampling.

Current acquisition/analysis architecture:
- deterministic multi-seed unique control reservoirs;
- control reuse across distinct case risk sets;
- primary cases frozen to the 3 literature-known SBs;
- provisional reservoir discoveries excluded from the primary case set until
  independent trajectory/B validation;
- acquisition artifact separated from offline analysis.

Current real acquisition:
- 603 records;
- 200 acquired controls per literature-known case;
- v7 artifact run: 35435974241;
- offline frozen-case analysis run: 35436185652.

Frozen-case result:
- 1:1: 3/3 cases matched, max abs SMD = 1.633;
- 1:4: 12 matched rows, max abs SMD = 2.417;
- neither passes abs SMD < 0.10.

Common-support diagnostic:
- EPR 1935: 197 eligible controls, minimum sleep-rate gap = 0.438;
- Washburn 1921: 198 eligible controls, minimum gap = 1.180;
- Hummers 1958: 195 eligible controls, minimum gap = 0.063.

Interpretation:
the current problem is not match yield but common support, especially in the
1921 stratum. Do not keep increasing the number of matched controls or relax
the SMD gate. Enumerate the complete exact field × year frame next.

Two provisional OpenAlex candidates have passed publisher identity/later-use
cross-checks but not independent annual-trajectory/B validation. They remain
provisional and are not primary cases.

Current blockers:
1. complete-frame common support has not yet been established;
2. OpenAlex B calibration is not source-validated;
3. OpenAlex live acquisition reached its current API rate window during the
   v8 reacquisition attempt; saved artifacts remain fully usable offline.

Therefore:
- mechanism_ready=true
- mechanism_analysis_ready=false

Do not run or report a substantive mechanism regression yet.

## Definition correction that must not be reverted

An earlier implementation tried to require early citation <=25th percentile and
late citation >=75th percentile for a paper to be called an SB. Real classic
cases showed that this is not a valid universal identity rule in sparse
historical cohorts: EPR and Washburn can rank high in relative early
percentiles while still showing decades-long low-rate sleep under absolute
trajectory definitions.

Current rule:
- robust SB identity = absolute/full-trajectory retrospective gate
- early/late percentile = separate descriptive quadrant
- post-awakening fate = separate descriptive dimension

Older percentile-gated identity text in historical notes is superseded.

## Post-awakening fate

Implemented states:
- TRANSIENT_OR_FADED
- ROUGHLY_SUSTAINED
- EXPANDED_AFTER_AWAKENING

This describes what happens after awakening and is not part of SB identity.
All three known cases in Pilot M v3 were EXPANDED_AFTER_AWAKENING.

## Temporal mechanism evidence

Mechanism signals are separated into:
- M0 publication-state evidence
- M1 sleep-period evidence
- M2 awakening-window evidence
- M3 post-awakening evidence

Anti-time-reversal rule:
A later event may help explain awakening, but cannot be used to explain why the
paper was initially overlooked without a separate longitudinal/causal design.

See agent/sleeping-beauty-miner/references/SIGNAL_CONTRACT.md.

## Current code that matters most

- code/mechanism_labels.py
  - robust gate
  - identity/quadrant separation
  - post-awakening fate
- code/mechanism_cohort.py
  - mechanism cohort builder/readiness gate
- code/mechanism_matching.py
  - secondary retrospective matching
- code/risk_set_matching.py
  - primary event-time dormant risk-set matching
- code/pilotM_known_case_enrichment.py
  - real known-case mechanism pilot
- code/openalex_adapter.py
  - full annual citation reconstruction and reproducible sampling
- code/sciscinet_adapter.py
  - cutoff-safe local SciSciNet-style adapter
- sql/
  - SciSciNet-v2 schema discovery and candidate-prefilter queries

## Data-access status

SciSciNet-v2 is the preferred large-corpus Track-A/Track-M backbone.
Executable SQL templates already exist:
- sql/sciscinet_v2_schema_discovery.sql
- sql/sciscinet_v2_sb_candidate_counts.sql
- sql/sciscinet_v2_sb_prefilter.sql

In the ChatGPT environment used on 2026-09-19, the BigQuery plugin existed but
was disabled by admin, so the SQL could not be executed directly from chat.
This is an environment/access constraint, not a scientific conclusion.

## Prospective Pilot 1 state

Already implemented:
- 10 field/era/seed strata
- 200 random historical papers
- 7 future-outcome definitions
- 5 transparent citation baselines
- recognition-floor sensitivity
- first lexical-novelty ablation

Current qualitative result:
- partial B is strong for future B-defined outcomes
- current citations/momentum are strong for future citation uptake
- no citation-only baseline consistently dominates delayed-recognition or
  awakening-consensus outcomes
- simple small-corpus lexical novelty did not stably improve the strongest
  citation baseline

Do not claim validated prospective prediction yet.

## Immediate next actions

1. Enumerate the **complete** same-field × same-publication-year OpenAlex frame
   for the 3 frozen literature-known cases; do not draw another random
   reservoir.
2. Re-run frozen 1:1 event-time support diagnostics with abs SMD < 0.10
   unchanged.
3. If complete-frame common support still fails, freeze an overlap-limited
   estimand or unmatched-case rule before any mechanism regression.
4. Independently validate OpenAlex annual citation trajectories / Beauty
   Coefficient using SciSciNet-v2 or another bibliographic source.
5. Add additional SBs to the primary case set only after cross-source
   trajectory/B validation.
6. Preserve acquisition/analysis separation: use saved artifacts for matcher
   development rather than repeatedly re-querying OpenAlex.
7. Only after acceptable balance, add mechanism feature families.
8. Keep M0/M1/M2/M3 timing explicit and continue Track B independently.

## CI / reproducibility checkpoint

Latest checked design-code CI:
- frozen primary-case selection: run 35436038223 — success;
- offline frozen-case reanalysis: run 35436139665 — success;
- offline common-support diagnostic path: success and checkpointed to
  data/pilotM_riskset_diagnostics_2026-09-19.json.

Live v8 reacquisition returned OpenAlex HTTP 429 after the rate window was
exhausted. Treat that as an acquisition constraint, not a scientific failure.

## Recovery instruction for a new chat

A new agent should begin with:

Read papers/015-sleeping-beauty-miner/process/HANDOFF.md and
process/STATUS.md, inspect the latest GitHub Actions for ARIS4C015, then
continue the immediate next actions without reverting the identity/quadrant
separation or the event-time risk-set design.

No information from the deleted chat is required to continue the current
scientific workflow.
