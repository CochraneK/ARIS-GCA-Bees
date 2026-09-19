# ARIS4C004 STATUS

Last updated: 2026-09-19

## Current state

**RUNNING — P4 pre-exposure audit / independent identity second-review gate**

P0 concept/causal architecture, P1 pilot30 feasibility, P2 frozen-100 identity expansion, and P3 frozen-100 work/network release are complete.

Mental-health exposure coding remains locked. The only scientific blocker to the final pre-exposure freeze is the independently executed identity second review and adjudication of any disagreements.

## Canonical question

Among historically realized knowledge contributors, how does scientific/intellectual/cultural development change when productive participation is counterfactually reduced, after allowing substitution, delays, and network rewiring — and what does that imply for exclusion risks faced by people with strong surviving mental-health evidence?

## Frozen 100-person identity frame

Canonical table: `data/derived/identity_decisions_100.csv`.

First-review states:

- candidates: **100**
- `VERIFIED_SINGLE`: **31**
- `VERIFIED_CLUSTER`: **21**
- verified total: **52**
- `NO_GRAPH_RECORD`: **38**
- `AMBIGUOUS_COLLISION`: **8**
- `EXCLUDED_IDENTITY_ERROR`: **2**
- `PROVISIONAL_*`: **0**

No mental-health information was used to construct or adjudicate this frame.

## P3 work/network gate — complete

Network100 acquisition successfully reconstructed the 52 verified identities:

- unique person-work records after deduplication: **2,956**
- fetch errors: **0**
- work shards: **8**

Every VERIFIED person now has a terminal work/network decision.

Final network-release state:

- **25/100 network-observable**
- **27 verified but network-unobservable**
  - 13 `HOLD_INSUFFICIENT_CLEAN_WORKS`
  - 14 `HOLD_UNRESOLVED_WORK_CONTAMINATION`

The unresolved-contamination hold is intentionally terminal for the pre-exposure frame. These people are not excluded as historical contributors; they are withheld from the confirmatory network frame because the person-level work corpus cannot be released at the frozen precision threshold without further attribution uncertainty.

No identity/work threshold was relaxed to increase N.

Canonical work decision table:
`data/derived/network100_person_work_decisions_v1.csv`.

## P4 observability audit — complete except independent second review

Frozen overall observability:

- verified identity rate: **52/100**
- network-observable rate: **25/100**
- no-graph: **38/100**
- collision: **8/100**
- identity error: **2/100**
- provisional: **0**

Frozen FORD network-observable rates:

| FORD broad field | N | Verified | Network-observable | Rate |
|---|---:|---:|---:|---:|
| Natural sciences | 27 | 15 | 8 | 29.6% |
| Engineering and technology | 7 | 2 | 1 | 14.3% |
| Medical and health sciences | 13 | 6 | 1 | 7.7% |
| Social sciences | 20 | 9 | 7 | 35.0% |
| Humanities and the arts | 16 | 10 | 2 | 12.5% |
| Unclassified | 17 | 10 | 6 | 35.3% |

These are **database/network observability differences**, not knowledge-importance differences.

Frozen audit outputs:

- `data/derived/observability_by_stratum.csv`
- `data/derived/observability_summary.json`
- `data/derived/ford_observability.csv`
- `data/derived/ford_observability_summary.json`
- `data/derived/ford_domains_frozen.csv`

## Independent identity second review — blocking gate

A deterministic blind second-review sample is frozen:

- selected: **40/100**
- all 21 `VERIFIED_CLUSTER`
- all 8 `AMBIGUOUS_COLLISION`
- all 2 `EXCLUDED_IDENTITY_ERROR`
- deterministic 9/31 `VERIFIED_SINGLE`

Blind assignment:
`data/derived/identity_second_review_blind_assignment.csv`

The independent reviewer has **not yet returned judgments**. The current assistant's own re-review cannot count as independent.

Exposure coding must not begin until the required external/independent review is returned and disagreements are adjudicated.

## Pilot30 network feasibility — passed

The pilot30 established the network architecture:

- 13 network-observable people
- 693 clean focal works
- 13/13 had downstream citation neighborhoods
- 897 temporally valid downstream edges
- 817 unique downstream person-work pairs
- 0 downstream temporal anomalies
- 0 API errors

The canonical graph object is a **person-specific temporal ego network**, not a pooled cross-field citation graph.

## Domain model

The upstream `Discovery/Science` source category is heterogeneous. OECD FORD stratification is frozen before exposure:

- Natural sciences: 27
- Engineering and technology: 7
- Medical and health sciences: 13
- Social sciences: 20
- Humanities and the arts: 16
- Unclassified: 17

Cross-domain raw citations/centrality are not interpreted as comparable impact.

## Alternate-frame decision

The canonical seed-20260918 frame will **not** be replaced before exposure coding.

A region- or FORD-balanced alternative frame is deferred as a versioned sensitivity/generalizability analysis only if exposure yield or common-support diagnostics later require it. This decision is pre-exposure and avoids outcome-driven frame repair.

## Completed

- [x] P0 concept / causal architecture.
- [x] P1 pilot30 identity/work/network feasibility.
- [x] P2 frozen-100 identity first review with zero provisional states.
- [x] Full network100 work acquisition: 2,956 unique works, 0 fetch errors.
- [x] P3 person-level work/network decisions for every VERIFIED identity.
- [x] Precision-first terminal holds for insufficient/contaminated work corpora.
- [x] Overall observability audit by cohort, visibility, region, gender and source subdomain.
- [x] OECD FORD domain stratification and observability audit.
- [x] Identity second-review sample and blind assignment frozen.
- [x] CI work/identity/data-integrity gates repaired and passing after dynamic-queue drift fix.
- [x] Decision made not to replace the canonical 100-person frame before exposure.

## Remaining before exposure coding

- [ ] Independent reviewer completes the frozen 40-person blind identity second review.
- [ ] Adjudicate any identity-state / Author-ID-set disagreements.
- [ ] Write and hash `PREEXPOSURE_FRAME_FREEZE.md`.

## Work that can proceed while the independent review is outstanding

- [ ] Simulator calibration/validation plan against empirical star-loss shocks.
- [ ] Simulation-based precision/N design.
- [ ] Closest-prior-work / novelty review packet.
- [ ] Preregistration/adversarial methods audit.
- [ ] Manuscript methods/limitations skeleton.

## Exposure gate

After P4 passes:

1. apply the frozen A1/A2/B1/B2/C/U exposure codebook;
2. independently review exposure classification / reliability;
3. quantify Tier-A and Tier-A+B yield;
4. treat U/unknown as unknown, never as healthy;
5. only then decide whether expansion beyond 100 is needed.

## Hard prohibitions

1. Do not hand-build a sample of famous people known to have psychiatric histories.
2. Do not start exposure coding before the independent identity gate and pre-exposure freeze.
3. Do not call unknown historical candidates healthy controls.
4. Do not lower identity/work thresholds to improve coverage.
5. Do not treat citation sparsity as low importance.
6. Do not compare raw cross-field citation centrality as intrinsic importance.
7. Do not treat participation simulations as direct proof of historical discrimination.
8. Do not claim contributions of people who left no observable historical trace are estimated by this design.

## Immediate next step

Complete all non-blocked P4/P6-method preparation while the frozen 40-person blind second review is handed to an independent reviewer. Once that file returns, adjudicate disagreements, freeze the pre-exposure frame, and move directly to exposure coding.
