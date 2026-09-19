# NETWORK100 WORK GATE FREEZE — ARIS4C004

Date: 2026-09-19  
Exposure status: **not coded / mental-health blind**

## Decision

The frozen 100-person first-review identity frame contains 52 VERIFIED identities.

The P3 work/network gate is now closed with a terminal decision for every VERIFIED identity.

| Work/network state | N |
|---|---:|
| Network-observable | **25** |
| Hold — insufficient clean works | **13** |
| Hold — unresolved work contamination | **14** |
| VERIFIED total | **52** |

No VERIFIED identity remains in an open-ended "keep reviewing until usable" state.

## Acquisition basis

The network100 acquisition reconstructed:

- 52 verified identities;
- **2,956** unique person-work records after person-level deduplication;
- **0** fetch errors;
- 8 recoverable work shards.

Raw OpenAlex `works_count` was never sufficient for release.

## Release evidence

Network release was allowed only under one of the frozen evidence paths:

1. existing pilot30 clean-work release;
2. deterministic MH-blind work-audit sample pass under the frozen audit rule;
3. explicit full-work review with every plausible row resolved and at least 5 KEEP works.

Machine priority signals never constituted a release/exclusion verdict.

Canonical person-level decision table:

`data/derived/network100_person_work_decisions_v1.csv`

Supporting evidence:

- `network100_reviewed_work_audit_evidence_v1.csv`
- `network100_full_work_review_v1.csv`
- `network100_held_work_audit_sample.csv`
- `network100_verified_work_summary.csv`
- `work_decisions_pilot30.csv`

## Terminal hold: insufficient clean works

`HOLD_INSUFFICIENT_CLEAN_WORKS` is used when the frozen work threshold cannot be met without relaxing the protocol.

These identities remain historically valid VERIFIED people but are network-unobservable in the confirmatory OpenAlex implementation.

The minimum 5-work rule is a pilot/analytic feasibility gate rather than an assertion that fewer works imply lower historical importance.

## Terminal hold: unresolved work contamination

`HOLD_UNRESOLVED_WORK_CONTAMINATION` is used when:

- >=5 mechanically plausible works exist, but
- unresolved namesake, fragment, posthumous-manifestation, container, or attribution uncertainty remains, and
- further review would primarily be an attempt to increase N rather than resolve a prespecified scientific necessity.

This is a **precision-first terminal hold**.

It does not mean:

- the person lacks influence;
- all attached works are wrong;
- the historical identity is unverified.

It means the work corpus is not clean enough for the confirmatory network frame under the frozen rule.

## Why the gate is closed at 25 rather than maximizing N

The study estimates counterfactual network effects. False work attribution can directly manufacture:

- spurious centrality;
- false citation descendants;
- fake cross-topic brokerage;
- artificial downstream persistence.

Therefore false inclusion is more damaging to the estimand than transparently documented missingness.

Coverage is characterized separately in the observability audit and is not repaired by loosening identity/work rules.

## Relationship to FORD/domain observability

The final 25/100 release rate is highly heterogeneous across FORD fields.

That heterogeneity is explicitly retained and reported rather than "balanced" by post hoc threshold changes.

Canonical observability outputs:

- `observability_by_stratum.csv`
- `observability_summary.json`
- `ford_observability.csv`
- `ford_observability_summary.json`

## Mental-health firewall

No mental-health evidence was used to:

- select the 100 candidates;
- verify identities;
- choose OpenAlex fragments;
- retain/exclude works;
- approve/hold network release;
- choose FORD fields;
- set observability thresholds.

These decisions are frozen before exposure coding.

## P3 exit

P3 is **COMPLETE**.

The 25 released people constitute the current pre-exposure network-observable analytic frame candidate.

P4 may alter identity mappings only through the prespecified independent second-review/adjudication process. It must not reopen held work corpora merely to increase sample size.
