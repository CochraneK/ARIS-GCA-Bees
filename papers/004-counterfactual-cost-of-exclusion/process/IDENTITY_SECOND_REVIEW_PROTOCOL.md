# IDENTITY SECOND-REVIEW PROTOCOL — ARIS4C004

Date frozen: 2026-09-18

## Purpose

Estimate and control identity-resolution error before any mental-health exposure coding or confirmatory CPE analysis.

The second reviewer must independently judge the historical person ↔ OpenAlex author/cluster mapping. The second review is not a proofreading pass over the first review.

## Selection

The second-review set is deterministic and fixed before exposure coding.

Always review:

- every `VERIFIED_CLUSTER`;
- every `AMBIGUOUS_COLLISION`;
- every `EXCLUDED_IDENTITY_ERROR`.

Additionally review a deterministic 25% sample of `VERIFIED_SINGLE` rows using:

- seed: `aris4c004-identity-second-review-v1`;
- SHA-256 of `seed|person_id`;
- inclusion if the resulting [0,1) fraction is < 0.25.

This avoids manually choosing apparently easy or difficult singles.

`NO_GRAPH_RECORD` cases are not part of the identity-precision sample by default because no positive OpenAlex identity mapping is being claimed. A separate missed-record audit may sample them later.

## Blinding

Second reviewers may see:

- canonical candidate identity metadata;
- birth/death dates;
- occupation/field;
- external authority identifiers and authority descriptions;
- candidate OpenAlex Author IDs and representative works;
- institutions, coauthors, topics, publication dates;
- source bibliographic records needed for identity.

Second reviewers must **not** see:

- mental-health evidence;
- exposure tier;
- CPE/network-removal result;
- whether a case would increase/decrease the final exposed sample.

Where operationally possible, the second-review packet should also hide the first review's final status and included Author IDs until the independent judgment is recorded.

## Second-review states

Use the same canonical identity states:

- `VERIFIED_SINGLE`
- `VERIFIED_CLUSTER`
- `AMBIGUOUS_COLLISION`
- `NO_GRAPH_RECORD`
- `EXCLUDED_IDENTITY_ERROR`

Do not create a weaker ad-hoc status to force agreement.

## Agreement

Exact agreement requires:

1. same identity state; and
2. for VERIFIED states, the same person-level set of included OpenAlex Author IDs.

Disagreement examples:

- single vs cluster;
- verified vs collision;
- same cluster status but different Author-ID membership;
- first reviewer excludes a fragment that second reviewer includes.

## Adjudication

Every disagreement is adjudicated before the person enters a confirmatory analytic frame.

Adjudication must record:

- evidence supporting each interpretation;
- final state;
- final Author-ID set;
- adjudicator;
- whether additional source retrieval was required.

No majority-by-model or confidence-score shortcut replaces evidence adjudication.

## Precision reporting

Report at minimum:

- number second-reviewed;
- exact state agreement;
- exact Author-ID-set agreement;
- false-positive identity mapping count;
- missed-fragment count;
- collision/error reversals;
- agreement separately for singles and clusters.

The goal is near-100% auditable precision for final included identities, not high raw resolver recall.

## Relationship to exposure coding

Mental-health exposure coding remains locked until:

1. identity/network frame is frozen;
2. difficult clusters have completed required second review/adjudication;
3. the deterministic single audit has been reviewed sufficiently to characterize error.

If identity precision is poor, improve identity methods or narrow the frame. Do not lower the identity gate to preserve sample size.
