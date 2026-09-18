# ARIS4C004 STATUS

Last updated: 2026-09-18

## Current state

**RUNNING — feasibility-pilot / verified-work-corpus gate**

The project has moved beyond concept-only design into a reproducible real-data science pilot. No mental-health exposure sample has yet been selected and no confirmatory CPE comparison has been run.

## Canonical question

Among historically realized knowledge contributors, how does scientific/intellectual/cultural development change when productive participation is counterfactually reduced, after allowing substitution, delays, and network rewiring — and what does that imply for exclusion risks faced by people with strong surviving mental-health evidence?

## Completed

- [x] Stable paper ID `004` and canonical folder created.
- [x] ARIS v0.4.26 provenance pinned to commit `951654847b015585385b2448c5667dcd04e7b56b`.
- [x] Core question reframed away from "mental illness causes genius."
- [x] Counterfactual changed from existence deletion to temporal participation attenuation.
- [x] Sign-neutral `CPE` estimand frozen; modeled effects may be positive, zero, or negative.
- [x] Naïve deletion demoted to a stress test; adaptive substitution/rewiring made mandatory.
- [x] Invisible-node / never-observed-excluded-person limitation explicitly bounded.
- [x] Causal/estimand audit added in `CAUSAL_MODEL.md`.
- [x] Mental-health evidence codebook frozen for pilot use: A1/A2/B1/B2/C/U; `Unknown != healthy`.
- [x] Deceased-only primary analysis rule frozen.
- [x] Historical celebrity examples separated from candidate-frame construction.
- [x] Three-domain portability concept specified; science/mathematics chosen as the primary quantitative route.
- [x] Data/licensing feasibility matrix completed.
- [x] GPTPage reviewer handoff packets completed.
- [x] Adversarial auto-review completed.
- [x] Minimal temporal M0/M1/M2 counterfactual simulator implemented.
- [x] GitHub CI smoke gate implemented and passing.
- [x] Real-data candidate-frame workflow implemented.
- [x] 108,626 eligible Discovery/Science source candidates identified.
- [x] Fixed-seed 100-person cohort × visibility pilot frame created without mental-health information.
- [x] Keyless OpenAlex pilot executed on first 30 candidates.
- [x] Mixed/legacy source-text encoding issue identified and corrected with reversible cell-level repair.
- [x] OpenAlex author fragmentation identified as a major identity-resolution problem.
- [x] Candidate-frame coverage and analytic-frame identity precision separated as distinct feasibility quantities.
- [x] Author-fragment review queue implemented; automatic top-hit matches no longer count as final identity verification.
- [x] Real pilot history recorded in `PILOT_RESULTS.md`.
- [x] `paper.json` synchronized to `feasibility-pilot` and portfolio rebuild triggered.

## Current real-data evidence

### Frozen pre-exposure frame

- 108,626 eligible Discovery/Science source candidates;
- 100-person fixed-seed frame (`20260918`) frozen before any mental-health search;
- first 30 used for the intensive identity pilot.

### Pilot30 identity freeze v1

Canonical decision table: `data/derived/identity_decisions_pilot30.csv`.

Final first-review identity states:

- `VERIFIED_SINGLE`: **11**
- `VERIFIED_CLUSTER`: **7**
- `NO_GRAPH_RECORD`: **9**
- `AMBIGUOUS_COLLISION`: **2**
- `EXCLUDED_IDENTITY_ERROR`: **1**
- `PROVISIONAL_*`: **0**

Thus **18/30 = 60%** have an externally auditable verified OpenAlex person mapping after first review. This is identity-resolution yield, not a population-coverage estimate and not yet an independently double-reviewed precision estimate.

Currently **9/30 = 30%** are released as `network_observable=true` under the pilot rules. A further 9 identities are verified but held back because of insufficient work count, posthumous/incorrect temporal metadata, duplicate fragments, or mixed-author work contamination.

The identity workflow discovered and fixed several data-engineering failure modes before exposure coding:

- 11/30 candidates required multi-Author-ID fragment review;
- 17/44 audited fragment profiles had >50% temporal contamination;
- weak shared coauthors/institutions produced false fragment support and are now guarded;
- a manual QID transcription error in the first decision-table draft was caught, corrected, and converted into a canonical-frame join invariant;
- unquoted commas in free-text CSV notes were caught, repaired, and converted into an extra-column validation invariant.

No mental-health information was used in any of these decisions.

See `IDENTITY_FREEZE_PILOT30.md` for the frozen milestone record.

## In progress

- [x] Complete first-review author/fragment adjudication on the first 30 candidates with zero provisional states.
- [x] Define and test person ↔ OpenAlex author-cluster validation rules.
- [x] Freeze pilot30 identity decision table and canonical-frame validation.
- [ ] Build and audit the verified-person work corpus (temporal flags + DOI/title deduplication + fragment provenance).
- [ ] Decontaminate mixed/duplicate verified records before releasing additional network-observable people.
- [ ] Run independent second-review audit of accepted identities / difficult clusters.
- [ ] Measure network observability by cohort, visibility, geography, gender and science subdomain.
- [ ] Decide whether candidate sampling needs explicit region/subdomain re-stratification.
- [ ] Freeze the network-observable analytic frame **before** mental-health coding.
- [ ] Pilot exposure coding and inter-rater reliability.
- [ ] Measure Tier-A / Tier-A+B exposure yield.
- [ ] Expand science sample using pilot-observed identity/exposure yield.
- [ ] Calibrate adaptive simulator against star-loss empirical benchmarks.
- [ ] Run simulation-based N / precision design.
- [ ] Run dedicated closest-prior-work novelty packet and final preregistration adversary.
- [ ] Audit humanities/arts portability only after science identity/network gate is stable.

## Revised feasibility gates

### Candidate-frame coverage gate

Do not require 95% of the broad historical frame to appear in OpenAlex. Instead:

- report graph observability and missingness by pre-exposure frame variables;
- require enough observable candidates in each retained stratum to support exposed/comparison analysis;
- do not improve coverage by loosening identity rules after seeing mental-health evidence.

### Analytic-frame identity gate

- every final included person must have an externally auditable identity decision;
- multiple plausible OpenAlex Author IDs require cluster review;
- conflicting ORCID/authority evidence blocks blind merging;
- final identity precision is prioritized over broad-frame coverage;
- a single automated top hit is never, by itself, confirmatory identity evidence.

### Exposure gate

- at least 15 Tier-A/Tier-B exposed focal cases in a domain pilot to justify domain expansion;
- strict primary exposure remains Tier A if final precision permits;
- candidate/network frame must be frozen before exposure search.

### Network gate

- sufficient domain-appropriate output/network data for preregistered baseline and downstream metrics;
- primary focal subgraphs require provenance and stable identity/edge construction;
- historical coverage bias must be characterized rather than hidden.

### Simulation gate

- M0/M1/M2 results stable over seeds and prespecified parameter ranges;
- no look-ahead substitute selection;
- strong null/random-subset benchmark required;
- negative CPE outcomes must remain reportable.

## Hard prohibitions

1. Do not hand-build a sample of famous people known to have psychiatric histories.
2. Do not start exposure coding before the network-observable frame is frozen.
3. Do not call unknown historical candidates "healthy controls."
4. Do not silently merge fragmented OpenAlex author records.
5. Do not lower identity thresholds merely to improve coverage.
6. Do not treat a participation simulation as proof of historical mental-health discrimination.
7. Do not pool raw science, philosophy/literature and arts network metrics into one universal importance score.
8. Do not claim to estimate contributions of people excluded before leaving observable historical traces.

## Next checkpoint

Advance from `feasibility-pilot` to `research-design` only when:

1. author-cluster identity protocol is stable and audited;
2. a pre-exposure science analytic frame is frozen;
3. Tier-A/Tier-B exposure-yield pilot is completed under the frozen codebook;
4. simulator calibration/validation plan has passed red-team review;
5. final confirmatory outcomes, matching families, intervention timing, and precision target are preregisterable without unresolved critical blockers.
