# ARIS4C004 STATUS

Last updated: 2026-09-18

## Current state

**RUNNING — pre-exposure scale-up / identity100 expansion**

The first-30 science pilot has passed identity, work-cleaning, and bounded downstream-network feasibility. The project is now expanding the same mental-health-blind identity/network pipeline to the full frozen 100-person science frame.

No mental-health exposure sample has yet been selected and no confirmatory CPE comparison has been run.

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
- [x] Mental-health evidence codebook frozen for later use: A1/A2/B1/B2/C/U; `Unknown != healthy`.
- [x] Deceased-only primary analysis rule frozen.
- [x] Historical celebrity examples separated from candidate-frame construction.
- [x] Three-domain portability concept specified; science/mathematics chosen as the primary quantitative route.
- [x] Data/licensing feasibility matrix completed.
- [x] GPTPage reviewer handoff packets and adversarial auto-review completed.
- [x] Minimal temporal M0/M1/M2 counterfactual simulator implemented.
- [x] GitHub CI smoke gate implemented and passing.
- [x] 108,626 eligible Discovery/Science source candidates identified.
- [x] Fixed-seed 100-person cohort × visibility frame frozen before mental-health search.
- [x] Mixed/legacy source-text encoding corrected with reversible cell-level repair.
- [x] Candidate-frame coverage and analytic-frame identity precision separated.
- [x] Pilot30 author fragmentation / identity protocol stabilized.
- [x] Pilot30 identity table frozen with zero provisional states.
- [x] Canonical-frame identity join validation added to CI.
- [x] Work-level codebook frozen before work cleanup.
- [x] 200/200 held-work decisions validated against regenerated OpenAlex review queue.
- [x] Pilot30 verified-person work corpus built: 18 verified people, 838 unique works, 0 fetch errors.
- [x] Four cleaned held identities released after work audit: Erika Greber, Joel Olson, Anton Moortgat, Fritz Strassmann.
- [x] Clean pre-exposure network frame built: 13 people / 693 clean works.
- [x] Time-reversed OpenAlex citation relations quarantined from the temporal graph.
- [x] Person-specific temporal ego-network architecture frozen in `NETWORK_MODEL.md`.
- [x] Bounded downstream citation feasibility passed for all 13 network-observable pilot people.
- [x] Citation-rich / citation-sparse network observability strata frozen before exposure coding.
- [x] Dedicated clean-network workflow split from the slower identity-discovery workflow.
- [x] MH-blind identity100 expansion workflow started.

## Current real-data evidence

### Frozen pre-exposure frame

- eligible Discovery/Science source candidates: **108,626**
- frozen science frame: **100**
- seed: `20260918`
- first intensive identity/network pilot: **30**

### Pilot30 identity freeze

Final first-review states:

- `VERIFIED_SINGLE`: **11**
- `VERIFIED_CLUSTER`: **7**
- `NO_GRAPH_RECORD`: **9**
- `AMBIGUOUS_COLLISION`: **2**
- `EXCLUDED_IDENTITY_ERROR`: **1**
- `PROVISIONAL_*`: **0**

Thus **18/30 = 60%** have a verified person ↔ OpenAlex mapping after first review.

### Pilot30 work/network release

After work-level cleaning:

- network-observable identities: **13/30 = 43.3%**
- clean focal works: **693**
- reference metadata coverage: **44.6%**
- external-coauthor metadata coverage: **63.1%**
- unique external coauthors: **395**
- institution metadata coverage: **48.1%**
- topic metadata coverage: **99.0%**
- build errors: **0**

Focal-only clean citation graph:

- valid temporal edges: **638**
- within-person edges: **638**
- cross-person focal edges: **0**
- quarantined time-reversed edges: **28**

The zero cross-person focal count is not treated as failure; the primary graph object is a person-specific temporal ego network.

### Bounded downstream ego-network pilot

Fixed pilot protocol:

- up to 6 deterministic anchors per person;
- earliest + temporal median + latest + highest-cited remaining;
- 20-year downstream horizon;
- max 50 citing works per anchor;
- earliest citing works acquired first.

Observed result:

- people: **13**
- anchors: **76**
- anchors with >=1 downstream citer: **52/76 = 68.4%**
- downstream edges: **897**
- unique downstream person-work pairs: **817**
- people with >=1 downstream work: **13/13**
- people with >=10 downstream works: **8/13**
- downstream temporal anomalies: **0**
- API errors: **0**

Citation-rich (>=10 downstream works): Albus, Olson, McWhinnie, Strassmann, Laksov, Gavron, Greber, Oelsen.

Citation-sparse (1–9): Carl Föhl, Ottomar Rosenbach, Friedrich Hoeth, Anton Moortgat, Hilario Hernández Gurruchaga.

Citation-sparse status is an observability label, **not an importance judgment**. These cases remain in the pre-exposure frame for multiplex/sensitivity analysis.

See:
- `IDENTITY_FREEZE_PILOT30.md`
- `WORK_CODEBOOK.md`
- `NETWORK_MODEL.md`
- `NETWORK_FEASIBILITY_PILOT30.md`

## In progress

- [x] Complete first-review identity adjudication on the first 30 with zero provisional states.
- [x] Build/audit verified-person work corpus and work-decision validator.
- [x] Decontaminate sufficient held identities to expand pilot network frame from 9 to 13.
- [x] Demonstrate bounded downstream citation neighborhoods for all 13.
- [ ] Resolve/triage the remaining 70 frozen candidates under the same MH-blind protocol.
- [ ] Produce and validate `identity_decisions_100_draft.csv`.
- [ ] Adjudicate new provisional single/cluster identities at scale.
- [ ] Build clean work corpora and network strata for newly verified identities.
- [ ] Measure final pre-exposure network observability by cohort, visibility, geography, gender and subdomain.
- [ ] Run independent second-review audit of accepted identities / difficult clusters.
- [ ] Decide whether an alternate region/subdomain sensitivity frame is required.
- [ ] Freeze the full network-observable analytic frame **before** mental-health coding.
- [ ] Pilot exposure coding and inter-rater reliability.
- [ ] Measure Tier-A / Tier-A+B exposure yield.
- [ ] Calibrate adaptive simulator against star-loss empirical benchmarks.
- [ ] Run simulation-based N / precision design.
- [ ] Run dedicated closest-prior-work novelty packet and final preregistration adversary.
- [ ] Audit humanities/arts portability only after the science frame is stable.

## Revised feasibility gates

### Candidate-frame coverage gate

Do not require 95% of the broad historical frame to appear in OpenAlex.

Instead:

- report graph observability and missingness by pre-exposure frame variables;
- require enough observable candidates in each retained stratum to support exposed/comparison analysis;
- do not improve coverage by loosening identity rules after seeing mental-health evidence.

### Analytic-frame identity gate

- every final included person must have an externally auditable identity decision;
- multiple plausible OpenAlex Author IDs require cluster review;
- conflicting ORCID/authority evidence blocks blind merging;
- final identity precision is prioritized over broad-frame coverage;
- a single automated top hit is never, by itself, confirmatory identity evidence.

### Work gate

- raw OpenAlex `works_count` never releases a person;
- explicit work decisions override raw author attribution;
- time-reversed citation edges are excluded from the temporal graph;
- modern reprints/container fragments/namesake works do not create historical production nodes.

### Network gate

Science-first feasibility has passed at pilot30.

For final scale-up:

- build person-specific temporal ego networks, not a pooled cross-field focal graph;
- retain citation-sparse people rather than deleting them for database undercoverage;
- standardize person-level CPE/network effects before cross-person comparison;
- characterize observability bias before exposure coding.

### Exposure gate

- candidate/network frame must be frozen before exposure search;
- at least 15 Tier-A/Tier-B exposed focal cases in the eventual domain frame to justify confirmatory expansion;
- strict primary exposure remains Tier A if final precision permits;
- `U` / unknown is never treated as healthy.

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
5. Do not lower identity/work thresholds merely to improve coverage.
6. Do not treat a participation simulation as proof of historical mental-health discrimination.
7. Do not pool raw science, philosophy/literature and arts network metrics into one universal importance score.
8. Do not compare raw citation centrality across unrelated fields as if it were intrinsic importance.
9. Do not claim to estimate contributions of people excluded before leaving observable historical traces.

## Next checkpoint

Advance from `feasibility-pilot` to `research-design` only when:

1. the full frozen science frame has a stable pre-exposure identity/network decision state;
2. observability bias is characterized across frame variables;
3. Tier-A/Tier-B exposure-yield pilot is completed under the frozen codebook;
4. simulator calibration/validation plan has passed red-team review;
5. final confirmatory outcomes, matching families, intervention timing, and precision target are preregisterable without unresolved critical blockers.
